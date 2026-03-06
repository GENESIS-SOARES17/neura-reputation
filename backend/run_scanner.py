#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Carrega variáveis de ambiente
load_dotenv()

from backend.scanner.blockchain_scanner import start_scanner

if __name__ == "__main__":
    print("Iniciando scanner blockchain...")
    start_scanner()
    print("Scanner finalizado.")