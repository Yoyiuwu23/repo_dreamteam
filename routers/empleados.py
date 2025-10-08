from fastapi import APIRouter, HTTPException
from dto.empleado import EmpleadoCreate, EmpleadoResponse
from models.empleados import EmpleadosModel
from typing import List

router = APIRouter(prefix="/empleados", tags=["Empleados"])

#GET api/v1/empleados
@router.get("/", response_model=List[EmpleadoResponse])
def list_empleados():
    return EmpleadosModel.get_all()


#POST api/v1/empleados
@router.post("/", response_model=EmpleadoResponse)
def create_empleado(empleado: EmpleadoCreate):
    #ver que llego:
    print(empleado)
    try:
        return EmpleadosModel.create(empleado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
