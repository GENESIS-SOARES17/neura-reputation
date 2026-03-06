import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.database import SessionLocal, Wallet, init_db
from backend.reputation_engine import calculate_reputation
from backend.ranking.ranking_engine import get_ranking

# Carrega variáveis do arquivo .env (apenas em desenvolvimento)
load_dotenv()

app = FastAPI()

# Configurar CORS (em produção, restrinja para o domínio do frontend)
allow_origins = os.getenv("ALLOW_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def home():
    return {"status": "Blockchain Reputation API Running"}

@app.get("/ranking")
def ranking(limit: int = 50):
    return get_ranking(limit)

@app.get("/analyze/{wallet}")
def analyze(wallet: str):
    if not wallet.startswith("0x") or len(wallet) != 42:
        raise HTTPException(status_code=400, detail="Endereço inválido")

    db = SessionLocal()
    try:
        wallet_db = db.query(Wallet).filter(Wallet.address == wallet).first()
        result = calculate_reputation(wallet, db)

        if wallet_db is None:
            wallet_db = Wallet(address=wallet)
            db.add(wallet_db)

        wallet_db.transaction_count = result["analysis"]["tx_count"]
        wallet_db.balance = result["analysis"]["balance"]
        wallet_db.age_score = result["analysis"]["age_score"]
        wallet_db.activity_score = result["analysis"]["activity_score"]
        wallet_db.liquidity_score = result["analysis"]["liquidity_score"]
        wallet_db.governance_score = result["analysis"]["governance_score"]
        wallet_db.reputation_score = result["reputation_score"]
        db.commit()

        return result
    finally:
        db.close()