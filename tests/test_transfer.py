import pytest
from pathlib import Path
import os
from inspect import currentframe

from ledger_app_clients.ethereum.client import EthAppClient
from .tron import TronClient
from .utils import get_appname_from_makefile, check_tx_signature
from ragger.navigator import NavInsID, NavIns
from ragger.backend import SpeculosBackend, BackendInterface

ROOT_SCREENSHOT_PATH = Path(__file__).parent
ABIS_FOLDER = "%s/abis" % (os.path.dirname(__file__))

PLUGIN_NAME = get_appname_from_makefile()

class TestTRX():
    '''Test TRX client.'''

    def configuration(self, backend: BackendInterface, navigator, firmware):
        if type(backend) is SpeculosBackend:
            if firmware.device == "flex":
                instructions = [
                    # Go to settings menu.
                    NavIns(NavInsID.USE_CASE_HOME_SETTINGS),
                    # Allow data in TXs
                    NavIns(NavInsID.TOUCH, (200, 150)),
                    # Allow custom contracts
                    NavIns(NavInsID.TOUCH, (200, 300)),
                    NavIns(NavInsID.USE_CASE_SETTINGS_NEXT),
                    # Allow sign by hash
                    NavIns(NavInsID.TOUCH, (200, 150)),
                    # Go back to main menu.
                    NavIns(NavInsID.USE_CASE_SETTINGS_MULTI_PAGE_EXIT),
                ]
            elif firmware.device == "stax":
                instructions = [
                    # Go to settings menu.
                    NavIns(NavInsID.USE_CASE_HOME_SETTINGS),
                    # Allow data in TXs
                    NavIns(NavInsID.TOUCH, (200, 150)),
                    # Allow custom contracts
                    NavIns(NavInsID.TOUCH, (200, 300)),
                    # Allow sign by hash
                    NavIns(NavInsID.TOUCH, (200, 450)),
                    # Go back to main menu.
                    NavIns(NavInsID.USE_CASE_SETTINGS_MULTI_PAGE_EXIT),
                ]
            else:
                instructions = [
                    # Go to settings main menu
                    NavInsID.RIGHT_CLICK,
                    NavInsID.RIGHT_CLICK,
                    NavInsID.BOTH_CLICK,
                    # Allow data in TXs
                    NavInsID.BOTH_CLICK,
                    # Allow custom contracts
                    NavInsID.RIGHT_CLICK,
                    NavInsID.BOTH_CLICK,
                    # Allow sign by hash
                    NavInsID.RIGHT_CLICK,
                    NavInsID.RIGHT_CLICK,
                    NavInsID.BOTH_CLICK,
                    # Go back to main menu
                    NavInsID.RIGHT_CLICK,
                    NavInsID.BOTH_CLICK,
                ]

            navigator.navigate(instructions,
                            screen_change_before_first_instruction=False)

    def clear_sign_and_validate(self, client, firmware, text_index, tx, signatures=[], navigate=True):
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

    def test_transfer(self, backend, firmware, navigator):
        client = EthAppClient(backend)

        # first setup the external plugin
        client.set_external_plugin(PLUGIN_NAME,
                                bytes.fromhex('410e1bce983f78f8913002c3f7e52daf78de6da2cb'),
                                bytes.fromhex('a9059cbb'),
                                bytes.fromhex('3045022100c6ed1e65f3c1a58fff2348c90e5945ae419e946f71142be6a5210333dd1d8ea7022010cdcf93e2895087194961c360ef24847c5c2c4c1956b02ece931fa4aed174ec'))

        client1 = TronClient(backend, firmware, navigator)
        tx = bytes.fromhex('0a02d20b220892915c91841dd16f40d097fec5f0315aae01081f12a9010a31747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e54726967676572536d617274436f6e747261637412740a15410dfba2397e8746cddd023d7670d8e0cdc1d497b81215410e1bce983f78f8913002c3f7e52daf78de6da2cb2244a9059cbb000000000000000000000000573708726db88a32c1b9c828fef508577cfb8483000000000000000000000000000000000000000000000000000000000000000a70dac5fac5f031900180ade204')
        self.clear_sign_and_validate(client1, firmware, 0, tx)
        # pytest ./tests/ -k "transfer" --tb=short -v --device nanosp --golden_run --log_apdu_file tests/test.log

    def test_multi_parts(self, backend, firmware, navigator):
        client = EthAppClient(backend)

        # # first setup the external plugin
        # client.set_external_plugin(PLUGIN_NAME,
        #                         bytes.fromhex('410e1bce983f78f8913002c3f7e52daf78de6da2cb'),
        #                         bytes.fromhex('a9059cbb'),
        #                         bytes.fromhex('3045022100c6ed1e65f3c1a58fff2348c90e5945ae419e946f71142be6a5210333dd1d8ea7022010cdcf93e2895087194961c360ef24847c5c2c4c1956b02ece931fa4aed174ec'))

        # first setup the external plugin
        client.set_external_plugin(PLUGIN_NAME,
                                bytes.fromhex('410e1bce983f78f8913002c3f7e52daf78de6da2cb'),
                                bytes.fromhex('38ed1739'))

        self.configuration(backend, navigator, firmware)

        client1 = TronClient(backend, firmware, navigator)
        # tx = bytes.fromhex("0a027dab220895bdfdbbd7c05c4840e8ccd88a813252ff017465737431746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746574657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573735ab001081f12a9010a31747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e54726967676572536d617274436f6e747261637412740a15410dfba2397e8746cddd023d7670d8e0cdc1d497b81215410e1bce983f78f8913002c3f7e52daf78de6da2cb2244a9059cbb000000000000000000000000fdb67e4809d920096050e4b0c7d4f8f2ea27f6990000000000000000000000000000000000000000000000000000000000000064286470acfcd48a8132900180ade204")
        tx = bytes.fromhex("0a02ec9f2208a838117fc1af203a40a88783b5813252ff017465737431746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746574657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573747465737474657374746573735ad202081f12cb020a31747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e54726967676572536d617274436f6e74726163741295020a15410dfba2397e8746cddd023d7670d8e0cdc1d497b81215410e1bce983f78f8913002c3f7e52daf78de6da2cb22e40138ed17390000000000000000000000000000000000000000000000c1d25decd18aa2b81b0000000000000000000000000000000000000000000000c1d25decd18aa2b81b00000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000573708726db88a32c1b9c828fef508577cfb848300000000000000000000000000000000000000000000000000000000611e29fd0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000fdb67e4809d920096050e4b0c7d4f8f2ea27f699286470c6b4ffb48132900180ade204")
        self.clear_sign_and_validate(client=client1, firmware=firmware, text_index=0, tx=tx, navigate=True)


        # pytest ./tests/ -k "multi_parts" --tb=short -v --device nanosp --golden_run --log_apdu_file tests/test.log