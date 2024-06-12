from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..crud import create_produto
from ..schemas import Produto, ProdutoCreate

router = APIRouter()

# Rota para criar um novo produto
@router.post("/produtos/", response_model=Produto)
def create_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    return create_produto(db, produto)