import os
from web3 import Web3
from sqlalchemy.orm import Session
from analyzers.wallet_age import calculate_wallet_age
from analyzers.activity import calculate_activity
from analyzers.liquidity import calculate_liquidity
from analyzers.governance import calculate_governance
from backend.database import Wallet

RPC_URL = os.getenv("RPC_URL", "https://testnet.rpc.neuraprotocol.io")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def calculate_reputation(wallet_address: str, db: Session = None):
    tx_count = w3.eth.get_transaction_count(wallet_address)
    balance_wei = w3.eth.get_balance(wallet_address)
    balance_eth = w3.from_wei(balance_wei, 'ether')

    first_tx_block = None
    last_tx_block = None
    if db:
        wallet_db = db.query(Wallet).filter(Wallet.address == wallet_address).first()
        if wallet_db:
            first_tx_block = wallet_db.first_tx_block
            last_tx_block = wallet_db.last_tx_block

    age_score = calculate_wallet_age(first_tx_block)
    activity_score = calculate_activity(tx_count, last_tx_block)
    liquidity_score = calculate_liquidity(wallet_address)
    governance_score = calculate_governance(wallet_address)

    total = age_score + activity_score + liquidity_score + governance_score
    reputation = min(total, 100)

    return {
        "wallet": wallet_address,
        "reputation_score": reputation,
        "analysis": {
            "balance": balance_eth,
            "tx_count": tx_count,
            "age_score": age_score,
            "activity_score": activity_score,
            "liquidity_score": liquidity_score,
            "governance_score": governance_score
        }
    }