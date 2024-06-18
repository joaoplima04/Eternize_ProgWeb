from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class Categoria(enum.Enum):
    PRATO_RASO = "Prato Raso"
    GUARDANAPO = "Guardanapo"
    TALHER = "Talher"
    TACAS = "Tacas"
    TRILHOS_DE_MESA = "Trilhos de Mesa"
    SOUSPLAT = "Sousplat"
    JOGO_AMERICANO = "Jogo Americano"
    CHA_E_CAFE = "Cha e Cafe"
    PRATO_SOBREMESA = "Prato Sobremesa"
    PORTA_GUARDANAPO = "Porta Guardanapo"

class Estilo(enum.Enum):
    ELEGANTE = "Elegante"
    TROPICAL = "Tropical"
    FLORIDO = "Florido"

class Produto(Base):
    __tablename__ = 'produto'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    categoria = Column(Enum(Categoria))
    preco = Column(Float)
    quantidade_estoque = Column(Integer, default=0)
    imagem = Column(String(255), nullable=True)
    cor = Column(String(100))
    estilo = Column(Enum(Estilo))
    publicado = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Produto(nome='{self.nome}', preco={self.preco}, quantidade_estoque={self.quantidade_estoque})>"

class Cliente(Base):
    __tablename__ = 'cliente'

    cpf = Column(String(11), primary_key=True)
    username = Column(String(150), unique=True)
    nome = Column(String(100))
    email = Column(String(255), unique=True)
    telefone = Column(String(20))
    data_nascimento = Column(Date)
    password = Column(String(128))

    def __repr__(self):
        return f"<Cliente(nome='{self.nome}', email='{self.email}')>"

class Aluguel(Base):
    __tablename__ = 'aluguel'

    id = Column(Integer, primary_key=True)
    cliente_cpf = Column(String(11), ForeignKey('cliente.cpf'))
    cliente = relationship("Cliente")
    data_aluguel = Column(Date)
    data_devolucao = Column(Date)
    preco_total = Column(Float)

    def __repr__(self):
        return f"<Aluguel(cliente_cpf='{self.cliente_cpf}', data_aluguel='{self.data_aluguel}', data_devolucao='{self.data_devolucao}', preco_total={self.preco_total})>"

class ItemCarrinho(Base):
    __tablename__ = 'itemCarrinho'

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey('produto.id'))
    quantidade = Column(Integer, nullable=False)

    produto = relationship("Produto")