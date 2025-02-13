from pydantic import BaseModel
from typing import Optional

class Conta(BaseModel):
    descricao: str
    valor: float
    vencimento: str  # Formato: YYYY-MM-DD
    categoria: str
    status: str  # "Pendente", "Pago", "Atrasado"
    forma_pagamento: Optional[str] = None
    pago_em: Optional[str] = None

