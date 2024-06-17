import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Produto, Categoria, Estilo

DATABASE_URL = "sqlite:///./test.db"  # Altere para sua URL de banco de dados

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def import_produtos_from_csv(csv_file):
    db = SessionLocal()
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            produto = Produto(
                id=int(row['id']),
                nome=row['nome'],
                categoria=Categoria[row['categoria']],
                preco=float(row['preco'].replace(',','.')),
                quantidade_estoque=int(row['quantidade_estoque']),
                imagem=row['imagem'],
                cor=row['cor'],
                estilo=Estilo[row['estilo']],
                publicado=row['publicado'].lower() == 'true'
            )
            try:
                db.add(produto)
            except:
                pass
        db.commit()
    db.close()

# Execute a função de importação
import_produtos_from_csv('produtos.csv')
