import os
from web3 import Web3

RPC_URL = os.getenv("RPC_URL", "https://testnet.rpc.neuraprotocol.io")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def calculate_wallet_age(first_tx_block: int = None):
    if first_tx_block is None:
        return 0

    try:
        latest_block = w3.eth.block_number
        blocks_passed = latest_block - first_tx_block
        age_score = min(blocks_passed / 10000, 25)
        return age_score
    except Exception:
        return 0