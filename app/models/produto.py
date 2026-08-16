from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId


class Produto(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    nome: str
    preco: float
    descricao: Optional[str] = None
    estoque: int

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


class ProdutoDbModel(Produto):
    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        if self.id:
            data["_id"] = str(self.id)
        return data
