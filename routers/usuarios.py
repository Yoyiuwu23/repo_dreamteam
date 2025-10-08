# routers/usuarios.py
from fastapi import APIRouter, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dto.usuario import UsuarioLogin, UsuarioResponse
from models.usuarios import UsuariosModel

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "titulo": "Login | Finantel Group", "error": None})

@router.post("/login", response_class=HTMLResponse)
def login_post(request: Request, email: str = Form(...), password: str = Form(...)):
    data = UsuarioLogin(email=email, password=password)
    usuario = UsuariosModel.authenticate(data)
    if not usuario:
        return templates.TemplateResponse("login.html", {"request": request, "titulo": "Login | Finantel Group", "error": "Credenciales inválidas"})
    # Pasa al home si login correcto
    return templates.TemplateResponse("home.html", {"request": request, "titulo": "Home | Finantel Group", "user": usuario})

# Ruta API para login por JSON (POST /usuarios/loginjson)
@router.post("/loginjson", response_model=UsuarioResponse)
def api_login(data: UsuarioLogin):
    usuario = UsuariosModel.authenticate(data)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return usuario
