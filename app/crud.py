from sqlalchemy.orm import Session
from . import models, schemas

# Funções CRUD para o modelo Produto

def get_produto(db: Session, produto_id: int):
    return db.query(models.Produto).filter(models.Produto.id == produto_id).first()

def get_produtos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Produto).offset(skip).limit(limit).all()

def create_produto(db: Session, produto: schemas.ProdutoCreate):
    db_produto = models.Produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

# Funções CRUD para o modelo Cliente

def get_cliente(db: Session, cliente_cpf: str):
    return db.query(models.Cliente).filter(models.Cliente.cpf == cliente_cpf).first()

def get_clientes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Funções CRUD para o modelo Aluguel

def get_aluguel(db: Session, aluguel_id: int):
    return db.query(models.Aluguel).filter(models.Aluguel.id == aluguel_id).first()

def get_alugueis(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Aluguel).offset(skip).limit(limit).all()

def create_aluguel(db: Session, aluguel: schemas.AluguelCreate):
    db_aluguel = models.Aluguel(**aluguel.dict())
    db.add(db_aluguel)
    db.commit()
    db.refresh(db_aluguel)
    return db_aluguel
