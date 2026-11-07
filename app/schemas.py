
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProdutoCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=40)
    nome: str = Field(min_length=1, max_length=120)
    margem_percentual: int = Field(default=30, ge=0, le=500)


class MargemUpdate(BaseModel):
    margem_percentual: int = Field(ge=0, le=500)


class CompraIn(BaseModel):
    quantidade: int = Field(gt=0)
    custo_unitario_centavos: int = Field(gt=0)


class SaidaIn(BaseModel):
    quantidade: int = Field(gt=0)


class ProdutoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    nome: str
    estoque: int
    custo_medio_centavos: int
    margem_percentual: int
    preco_venda_centavos: int


class MovimentacaoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo: str
    quantidade: int
    custo_unitario_centavos: int | None
    criado_em: datetime
