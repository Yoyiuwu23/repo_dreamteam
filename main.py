# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import empleados, public, usuarios
from routers import empleados, public, usuarios, liquidacion

app = FastAPI(title="Finantel Group")

app.mount(
    "/assets",   
    StaticFiles(directory="templates/assets"),
    name="assets"
)
# Rutas privadas y públicas
app.include_router(empleados.router, prefix="/api/v1")    # empleados API
app.include_router(public.router)                         # landing y páginas públicas
app.include_router(usuarios.router)                       # login y login API
app.include_router(liquidacion.router, prefix="/api/v1")  # liquidacion API
