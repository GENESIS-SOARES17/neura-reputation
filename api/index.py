# api/index.py
# Entrypoint para o Vercel – expõe a aplicação FastAPI

import sys
import os

# Adiciona a raiz do projeto ao path para que os pacotes backend e analyzers sejam encontrados
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app

# A variável 'app' é o ASGI app que o Vercel irá executar