# routers/liquidacion.py
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from dto.liquidacion import LiquidacionCreate, LiquidacionResponse
from models.liquidacion import LiquidacionModel
from util.liquidacion_service import LiquidacionService
from typing import List
import os

router = APIRouter(prefix="/liquidacion", tags=["Liquidacion"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=List[LiquidacionResponse])
def get_liquidaciones():
    """GET: Obtiene todas las liquidaciones"""
    return LiquidacionModel.get_all()

@router.post("/", response_model=LiquidacionResponse)
def create_liquidacion(liquidacion: LiquidacionCreate):
    """POST: Crea una nueva liquidación"""
    try:
        return LiquidacionModel.create(liquidacion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pdf", response_class=FileResponse)
def generar_pdf_liquidaciones():
    """
    GET: Genera un PDF con todas las liquidaciones
    Este endpoint obtiene los datos (GET) y los imprime en PDF
    """
    try:
        # GET: Obtener los datos
        liquidaciones = LiquidacionModel.get_all()
        
        if not liquidaciones:
            raise HTTPException(status_code=404, detail="No hay liquidaciones disponibles")
        
        # Generar PDF con el servicio
        filepath = LiquidacionService.generar_pdf(liquidaciones)
        
        # Retornar el archivo
        return FileResponse(
            filepath,
            media_type='application/pdf',
            filename=os.path.basename(filepath),
            headers={"Content-Disposition": f"attachment; filename={os.path.basename(filepath)}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar PDF: {str(e)}")

@router.get("/vista", response_class=HTMLResponse)
def liquidaciones_vista(request: Request):
    """Vista HTML para mostrar y generar liquidaciones"""
    liquidaciones = LiquidacionModel.get_all()
    return templates.TemplateResponse("liquidaciones.html", {
        "request": request,
        "titulo": "Liquidaciones | Finantel Group",
        "liquidaciones": liquidaciones
    })
