from pydantic import BaseModel
from datetime import date


class Venda(BaseModel):
    data_venda: date
    id_produto: str
    quantidade: int
    valor_total: float
