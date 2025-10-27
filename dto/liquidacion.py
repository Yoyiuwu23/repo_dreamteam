# dto/liquidacion.py
from pydantic import BaseModel
from typing import Optional

class LiquidacionCreate(BaseModel):
    nombre: str
    rut: str
    cargo: str
    sueldo_base: float
    horas_extras: float = 0.0

class LiquidacionResponse(LiquidacionCreate):
    id: int
    total: Optional[float] = None
    
    def calcular_total(self):
        """Calcula el total sumando sueldo base + horas extras"""
        self.total = self.sueldo_base + self.horas_extras
        return self.total
