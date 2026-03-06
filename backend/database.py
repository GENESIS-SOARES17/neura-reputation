import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

# Obtém a URL do banco de dados da variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/neura_reputation.db")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True, nullable=False)

    transaction_count = Column(Integer, default=0)
    total_volume = Column(Float, default=0.0)
    balance = Column(Float, default=0.0)
    first_tx_block = Column(Integer, nullable=True)
    last_tx_block = Column(Integer, nullable=True)

    age_score = Column(Float, default=0.0)
    activity_score = Column(Float, default=0.0)
    liquidity_score = Column(Float, default=0.0)
    governance_score = Column(Float, default=0.0)
    reputation_score = Column(Float, default=0.0)

    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)