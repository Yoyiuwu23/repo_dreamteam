# routers/empleados.py
from fastapi import APIRouter, HTTPException
from dto.empleado import EmpleadoCreate, EmpleadoResponse
from models.empleados import EmpleadosModel
from typing import List

router = APIRouter(prefix="/empleados", tags=["Empleados"])

@router.get("/", response_model=List[EmpleadoResponse])
def list_empleados():
    return EmpleadosModel.get_all()

@router.post("/", response_model=EmpleadoResponse)
def create_empleado(empleado: EmpleadoCreate):
    try:
        return EmpleadosModel.create(empleado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
