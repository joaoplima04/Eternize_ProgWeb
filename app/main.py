from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import auth, users, cart, products
from pathlib import Path

#from .database import init_db
from .routers import auth, users, cart, products, categories

app = FastAPI()

static_files_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Create the database tables
#@app.on_event("startup")
#def on_startup():
#   init_db()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("categorias/index.html", {"request": request})

app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(users.router, prefix="/users", tags=["users"])

'''
# Include routers for different modules
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
'''