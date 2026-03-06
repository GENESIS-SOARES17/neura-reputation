from sqlalchemy.orm import Session
from backend.database import SessionLocal, Wallet

def get_ranking(limit: int = 50):
    """
    Retorna as top 'limit' carteiras com maior reputation_score.
    Formato: lista de dicionários [{"wallet": "0x...", "score": 99.5}, ...]
    """
    db: Session = SessionLocal()
    try:
        wallets = db.query(Wallet).order_by(Wallet.reputation_score.desc()).limit(limit).all()
        ranking = [
            {
                "wallet": w.address,
                "score": w.reputation_score
            }
            for w in wallets
        ]
        return ranking
    finally:
        db.close()