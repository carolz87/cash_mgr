from fastapi import FastAPI,  HTTPException
from pymongo import MongoClient
from bson import ObjectId
from typing import List
import DATA.models as c
import dotenv
import os

dotenv.load_dotenv()

# Conectando ao MongoDB
client = MongoClient(os.getenv('URI'))
db = client[os.getenv('DATABASE_NAME')]
contas_collection = db["contas"]

# Inicializando a API
app = FastAPI()


# Criar uma conta (CREATE)
@app.post("/contas/", response_model=dict)
def criar_conta(conta: c.Conta):
    nova_conta = conta.model_dump()
    result = contas_collection.insert_one(nova_conta)
    return {"id": str(result.inserted_id), "mensagem": "Conta cadastrada com sucesso"}

# Listar todas as contas (READ)
@app.get("/contas/", response_model=List[dict])
def listar_contas():
    contas = list(contas_collection.find({}, {"_id": 1, "descricao": 1, "valor": 1, "vencimento": 1, "status": 1}))
    for conta in contas:
        conta["_id"] = str(conta["_id"])  # Convertendo ObjectId para string
    return contas

# Atualizar uma conta por ID (UPDATE)
@app.put("/contas/{conta_id}", response_model=dict)
def atualizar_conta(conta_id: str, conta: c.Conta):
    result = contas_collection.update_one({"_id": ObjectId(conta_id)}, {"$set": conta.model_dump()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return {"mensagem": "Conta atualizada com sucesso"}

# Deletar uma conta por ID (DELETE)
@app.delete("/contas/{conta_id}", response_model=dict)
def deletar_conta(conta_id: str):
    result = contas_collection.delete_one({"_id": ObjectId(conta_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return {"mensagem": "Conta deletada com sucesso"}

@app.get("/")
def home():
    return {"message": "API de Controle Financeiro está rodando!"}

