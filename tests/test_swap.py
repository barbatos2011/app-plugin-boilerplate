from pathlib import Path
import json
import os
import datetime

from web3 import Web3
from eth_typing import ChainId

from ledger_app_clients.ethereum.client import EthAppClient
from ledger_app_clients.ethereum.utils import get_selector_from_data

from .utils import get_appname_from_makefile


ROOT_SCREENSHOT_PATH = Path(__file__).parent
ABIS_FOLDER = "%s/abis" % (os.path.dirname(__file__))

PLUGIN_NAME = get_appname_from_makefile()


with open("%s/0x000102030405060708090a0b0c0d0e0f10111213.abi.json" % (ABIS_FOLDER)) as file:
    contract = Web3().eth.contract(
        abi=json.load(file),
        # Get address from filename
        address=bytes.fromhex(os.path.basename(file.name).split(".")[0].split("x")[-1])
    )


# EDIT THIS: build your own test
def test_swap_exact_eth_for_token(backend, firmware, navigator):
    client = EthAppClient(backend)

    data = contract.encodeABI("swapExactETHForTokens", [
        Web3.to_wei(28.5, "ether"),
        [
            bytes.fromhex("C02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"),
            bytes.fromhex("6B3595068778DD592e39A122f4f5a5cF09C90fE2")
        ],
        bytes.fromhex("d8dA6BF26964aF9D7eEd9e03E53415D37aA96045"),
        int(datetime.datetime(2023, 12, 25, 0, 0).timestamp())
    ])

    # first setup the external plugin
    client.set_external_plugin(PLUGIN_NAME,
                               contract.address,
                               # Extract function selector from the encoded data
                               get_selector_from_data(data))
