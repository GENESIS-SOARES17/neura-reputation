import os
from web3 import Web3

RPC_URL = os.getenv("RPC_URL", "https://testnet.rpc.neuraprotocol.io")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def calculate_activity(transaction_count: int, last_tx_block: int = None):
    if transaction_count == 0:
        return 0

    try:
        base = min(transaction_count * 0.05, 20)

        bonus = 0
        if last_tx_block:
            latest = w3.eth.block_number
            blocks_ago = latest - last_tx_block
            if blocks_ago < 1000:
                bonus = 10
            elif blocks_ago < 10000:
                bonus = 5
            elif blocks_ago < 50000:
                bonus = 2

        return min(base + bonus, 30)
    except Exception:
        return 0