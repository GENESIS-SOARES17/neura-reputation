@echo off
cd /d "D:\BACKUP\MeusProjetos\Sistema de Reputação On-Chain"
echo Instalando dependências...
pip install -r requirements.txt
echo Iniciando servidor FastAPI...
start cmd /k "uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3
echo Abrindo frontend...
start http://127.0.0.1:8000
echo Para executar o scanner: python backend/run_scanner.py
pause