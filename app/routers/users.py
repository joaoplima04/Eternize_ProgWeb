from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import schemas, crud, auth
from ..database import get_db
from ..config import templates
from typing import Optional

router = APIRouter()

@router.get("/cadastro", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("categorias/cadastro.html", {"request": request})

def get_cliente_form(
    cpf: str = Form(...),
    username: str = Form(...),
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    data_nascimento: str = Form(...),
    password: str = Form(...)
) -> schemas.ClienteCreate:
    return schemas.ClienteCreate(
        cpf=cpf,
        username=username,
        nome=nome,
        email=email,
        telefone=telefone,
        data_nascimento=data_nascimento,
        password=password
    )

@router.post("/cadastro_user/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteCreate = Depends(get_cliente_form), db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, cliente_email=cliente.email)
    if db_cliente:
        raise HTTPException(status_code=400, detail="CPF já registrado")
    new_cliente = crud.create_cliente(db=db, cliente=cliente)

    access_token = auth.create_access_token(data={"sub": new_cliente.email}, expires_delta=timedelta(minutes=60))
    # Redireciona para a página principal com uma mensagem de boas-vindas
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=3600)
    response.set_cookie(key="welcome_message", value=f"Bem vindo {new_cliente.nome}!", max_age=3600)
    return response

@router.get("/login", response_class=HTMLResponse)
def get_login(request: Request, token: Optional[str] = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user = auth.get_current_user(token, db)
        if user:
            context = {
                "message": "Seu login já está ativo! Deseja Fazer o logoff?",
                "request": request
            }
            return templates.TemplateResponse("categorias/login.html", context)
    except HTTPException as e:
        raise f"O erro é {e}"

    error = request.cookies.get("error")
    context = {"request": request}
    if error:
        context["error"] = error
    return templates.TemplateResponse("categorias/login.html", context)

@router.post("/login_user/")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud.get_cliente(db, cliente_email=email)
    if not user:
        response = RedirectResponse(url="/users/login", status_code=303)
        response.set_cookie(key="error", value=f"Email incorreto", max_age=3600)
        return response
    if not auth.verify_password(password, user.password):
        response = RedirectResponse(url="/users/login", status_code=303)
        response.set_cookie(key="error", value=f"senha incorreta", max_age=3600)
        return response
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="welcome_message", value=f"Bem vindo {user.nome}!", max_age=3600)
    return response

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="Authorization")
    return response