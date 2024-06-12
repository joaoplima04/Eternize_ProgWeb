from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ProdutoBase(BaseModel):
    nome: str
    categoria: str
    preco: float
    quantidade_estoque: int
    imagem: Optional[str] = None
    cor: str
    estilo: str
    publicado: bool

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int

    class Config:
        orm_mode = True

class ClienteBase(BaseModel):
    cpf: str
    username: str
    nome: str
    email: str
    telefone: str
    data_nascimento: date

class ClienteCreate(ClienteBase):
    password: str

class Cliente(ClienteBase):
    class Config:
        orm_mode = True

class AluguelBase(BaseModel):
    cliente_cpf: str
    data_aluguel: date
    data_devolucao: date
    preco_total: float

class AluguelCreate(AluguelBase):
    pass

class Aluguel(AluguelBase):
    id: int

    class Config:
        orm_mode = True
