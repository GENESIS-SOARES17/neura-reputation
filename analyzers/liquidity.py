import os
from web3 import Web3

RPC_URL = os.getenv("RPC_URL", "https://testnet.rpc.neuraprotocol.io")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def calculate_liquidity(wallet: str):
    try:
        balance_wei = w3.eth.get_balance(wallet)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        score = min(balance_eth * 2.5, 25)
        return score
    except Exception:
        return 0