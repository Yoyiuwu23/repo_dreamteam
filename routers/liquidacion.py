# routers/liquidacion.py
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from dto.liquidacion import LiquidacionCreate, LiquidacionResponse
from models.liquidacion import LiquidacionModel
from util.liquidacion_service import LiquidacionService
from typing import List
from datetime import datetime
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

@router.get("/pdf/{empleado_id}", response_class=FileResponse)
def generar_pdf_liquidacion(empleado_id: int):
    """
    GET: Genera un PDF con la liquidación de un empleado específico
    Este endpoint obtiene los datos (GET) por ID y los imprime en PDF
    """
    try:
        # GET: Obtener los datos del empleado específico
        liquidacion = LiquidacionModel.get_by_id(empleado_id)
        
        if not liquidacion:
            raise HTTPException(status_code=404, detail=f"No se encontró la liquidación para el empleado {empleado_id}")
        
        # Generar PDF con el servicio (enviamos como lista de un elemento)
        filepath = LiquidacionService.generar_pdf([liquidacion])
        
        # Retornar el archivo
        return FileResponse(
            filepath,
            media_type='application/pdf',
            filename=f"liquidacion_{empleado_id}_{datetime.now().strftime('%Y%m%d')}.pdf",
            headers={"Content-Disposition": f"attachment; filename=liquidacion_{empleado_id}.pdf"}
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
