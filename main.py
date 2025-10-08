from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import empleados, public
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount(
    "/assets",  
    StaticFiles(directory="templates/assets"),
    name="assets"
)
templates = Jinja2Templates(directory="templates")  
# Rutas privadas 
app.include_router(empleados.router, prefix="/api/v1")
# Rutas públicas
app.include_router(public.router)
