import os
import time
from web3 import Web3
from backend.database import SessionLocal, Wallet

RPC_URL = os.getenv("RPC_URL", "https://testnet.rpc.neuraprotocol.io")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

LAST_BLOCK_FILE = os.path.join(os.path.dirname(__file__), "last_block.txt")

def get_last_scanned_block() -> int:
    try:
        with open(LAST_BLOCK_FILE, "r") as f:
            return int(f.read().strip())
    except:
        latest = w3.eth.block_number
        return max(latest - 1000, 0)

def set_last_scanned_block(block: int):
    with open(LAST_BLOCK_FILE, "w") as f:
        f.write(str(block))

def update_wallet_from_tx(db, address: str, tx_value_eth: float, tx_block: int):
    wallet = db.query(Wallet).filter(Wallet.address == address).first()
    if not wallet:
        wallet = Wallet(address=address)
        db.add(wallet)
        db.flush()

    wallet.transaction_count = (wallet.transaction_count or 0) + 1
    wallet.total_volume = (wallet.total_volume or 0) + tx_value_eth

    if wallet.first_tx_block is None or tx_block < wallet.first_tx_block:
        wallet.first_tx_block = tx_block
    if wallet.last_tx_block is None or tx_block > wallet.last_tx_block:
        wallet.last_tx_block = tx_block

def scan_block(block_number: int, db):
    try:
        block = w3.eth.get_block(block_number, full_transactions=True)
        processed_addresses = set()

        for tx in block.transactions:
            value_eth = w3.from_wei(tx.get('value', 0), 'ether')
            from_addr = tx.get('from')
            if from_addr and from_addr not in processed_addresses:
                update_wallet_from_tx(db, from_addr, value_eth, block_number)
                processed_addresses.add(from_addr)

            to_addr = tx.get('to')
            if to_addr and to_addr not in processed_addresses:
                update_wallet_from_tx(db, to_addr, value_eth, block_number)
                processed_addresses.add(to_addr)

        db.commit()
        print(f"Bloco {block_number} processado: {len(processed_addresses)} carteiras atualizadas.")
    except Exception as e:
        db.rollback()
        print(f"Erro ao processar bloco {block_number}: {e}")

def start_scanner():
    db = SessionLocal()
    try:
        latest = w3.eth.block_number
        last_scanned = get_last_scanned_block()
        print(f"Último bloco escaneado: {last_scanned}. Atual: {latest}")

        if last_scanned >= latest:
            print("Nenhum bloco novo para escanear.")
            return

        for block in range(last_scanned + 1, latest + 1):
            scan_block(block, db)
            set_last_scanned_block(block)
            time.sleep(0.2)
    finally:
        db.close()