from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, auth
from ..database import get_db

router = APIRouter()

@router.post("/register/", response_model=schemas.Cliente)
def register_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente_by_email(db, email=cliente.email)
    if db_cliente:
        raise HTTPException(status_code=400, detail="E-mail já registrado")
    return crud.create_cliente(db=db, cliente=cliente)

@router.post("/login/")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_cliente_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    if not auth.verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}