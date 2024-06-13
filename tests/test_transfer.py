from pathlib import Path
import os
from inspect import currentframe

from ledger_app_clients.ethereum.client import EthAppClient
from .tron import TronClient
from .utils import get_appname_from_makefile, check_tx_signature


ROOT_SCREENSHOT_PATH = Path(__file__).parent
ABIS_FOLDER = "%s/abis" % (os.path.dirname(__file__))

PLUGIN_NAME = get_appname_from_makefile()

def clear_sign_and_validate(client, firmware, text_index, tx, signatures=[], navigate=True):
    path = Path(currentframe().f_back.f_code.co_name)
    text = None
    if firmware.device.startswith("nano"):
        if text_index == 0:
            text = "Sign"
        elif text_index == 1:
            text = "Accept"
    else:
        if text_index == 0 or text_index == 1:
            text = "Hold to sign"
    assert text
    resp = client.clear_sign(client.getAccount(0)['path'],
                        tx,
                        signatures=signatures,
                        snappath=path,
                        text=text,
                        navigate=navigate)
    assert check_tx_signature(tx, resp.data[0:65],
                                client.getAccount(0)['publicKey'][2:])

def test_transfer(backend, firmware, navigator):
    client = EthAppClient(backend)

    # first setup the external plugin
    client.set_external_plugin(PLUGIN_NAME,
                            bytes.fromhex('410e1bce983f78f8913002c3f7e52daf78de6da2cb'),
                            bytes.fromhex('a9059cbb'),
                            bytes.fromhex('3045022100c6ed1e65f3c1a58fff2348c90e5945ae419e946f71142be6a5210333dd1d8ea7022010cdcf93e2895087194961c360ef24847c5c2c4c1956b02ece931fa4aed174ec'))

    client1 = TronClient(backend, firmware, navigator)
    tx = bytes.fromhex('0a02d20b220892915c91841dd16f40d097fec5f0315aae01081f12a9010a31747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e54726967676572536d617274436f6e747261637412740a15410dfba2397e8746cddd023d7670d8e0cdc1d497b81215410e1bce983f78f8913002c3f7e52daf78de6da2cb2244a9059cbb000000000000000000000000573708726db88a32c1b9c828fef508577cfb8483000000000000000000000000000000000000000000000000000000000000000a70dac5fac5f031900180ade204')
    clear_sign_and_validate(client1, firmware, 0, tx)
    # pytest ./tests/ -k "transfer" --tb=short -v --device nanosp --golden_run --log_apdu_file tests/test.log


def test_multi_parts(backend, firmware, navigator):
    client = EthAppClient(backend)

    # first setup the external plugin
    client.set_external_plugin(PLUGIN_NAME,
                            bytes.fromhex('410e1bce983f78f8913002c3f7e52daf78de6da2cb'),
                            bytes.fromhex('a9059cbb'),
                            bytes.fromhex('3045022100c6ed1e65f3c1a58fff2348c90e5945ae419e946f71142be6a5210333dd1d8ea7022010cdcf93e2895087194961c360ef24847c5c2c4c1956b02ece931fa4aed174ec'))

    client1 = TronClient(backend, firmware, navigator)
    tx = bytes.fromhex('0a02d20b220892915c91841dd16f40d097fec5f0315aae01081f12a9010a31747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e54726967676572536d617274436f6e747261637412740a15410dfba2397e8746cddd023d7670d8e0cdc1d497b81215410e1bce983f78f8913002c3f7e52daf78de6da2cb2244a9059cbb000000000000000000000000573708726db88a32c1b9c828fef508577cfb8483000000000000000000000000000000000000000000000000000000000000000a70dac5fac5f031900180ade204')
    clear_sign_and_validate(client1, firmware, 0, tx, navigate=True)


    # pytest ./tests/ -k "multi_parts" --tb=short -v --device nanosp --golden_run --log_apdu_file tests/test.log