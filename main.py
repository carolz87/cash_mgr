from fastapi import FastAPI
from pymongo import MongoClient
import dotenv
import os

dotenv.load_dotenv()

# Conectando ao MongoDB
client = MongoClient(os.getenv('URI'))
db = client[os.getenv('DATABASE_NAME')]

# Inicializando a API
app = FastAPI()

# Teste de rota
@app.get("/")
def home():
    return {"message": "API de Controle Financeiro está rodando!"}
