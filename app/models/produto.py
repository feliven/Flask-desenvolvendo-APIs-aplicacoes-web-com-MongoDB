from pydantic import BaseModel
from typing import Optional


class Produto(BaseModel):
    nome: str
    preco: float
    descricao: Optional[str] = None
    estoque: int

    class Config:
        from_attributes = True
