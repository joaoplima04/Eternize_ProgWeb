from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import Produto, ProdutoCreate

router = APIRouter()

@router.get("/categoria/{categoria_name}/", response_class=HTMLResponse)
def read_categoria(request: Request, categoria_name: str, db: Session = Depends(get_db)):
    # Implemente a lógica para filtrar produtos por categoria
    produtos = db.query(Produto).filter(Produto.categoria == categoria_name, Produto.publicado == True).all()
    return templates.TemplateResponse("categoria.html", {"request": request, "produtos": produtos, "categoria": categoria_name})
