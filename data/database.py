# backend/database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")  # pasta data na raiz
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'neura_reputation.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True, nullable=False)

    # Dados brutos
    transaction_count = Column(Integer, default=0)
    total_volume = Column(Float, default=0.0)          # soma de valores enviados/recebidos
    balance = Column(Float, default=0.0)               # saldo atual (pode ser atualizado periodicamente)
    first_tx_block = Column(Integer, nullable=True)    # bloco da primeira transação
    last_tx_block = Column(Integer, nullable=True)      # último bloco com transação

    # Scores individuais (calculados)
    age_score = Column(Float, default=0.0)
    activity_score = Column(Float, default=0.0)
    liquidity_score = Column(Float, default=0.0)
    governance_score = Column(Float, default=0.0)
    reputation_score = Column(Float, default=0.0)

    # Metadados
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)