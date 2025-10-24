# models/liquidacion.py
from core.database import get_connection
from dto.liquidacion import LiquidacionCreate, LiquidacionResponse
from typing import List

class LiquidacionModel:
    @staticmethod
    def get_all() -> List[LiquidacionResponse]:
        """GET: Obtiene todas las liquidaciones de la base de datos"""
        cnx = get_connection()
        if not cnx:
            return []
        
        cursor = cnx.cursor(dictionary=True)
        try:
            # Consulta para obtener datos de liquidaciones
            cursor.execute(
                """
                SELECT 
                    e.id,
                    CONCAT(e.nombres, ' ', e.apellidos) as nombre,
                    e.rut,
                    'Empleado' as cargo,
                    c.sueldo_base,
                    0 as horas_extras
                FROM empleados e
                JOIN contratos c ON e.id = c.empleado_id
                """
            )
            liquidaciones = cursor.fetchall()
            
            # Calcular totales
            result = []
            for liq in liquidaciones:
                liquidacion = LiquidacionResponse(**liq)
                liquidacion.calcular_total()
                result.append(liquidacion)
            
            return result
        finally:
            cursor.close()
            cnx.close()
    
    @staticmethod
    def create(liquidacion: LiquidacionCreate) -> LiquidacionResponse:
        """POST: Crea una nueva liquidación en la base de datos"""
        cnx = get_connection()
        if not cnx:
            raise Exception("No se pudo conectar a la base de datos")
        
        cursor = cnx.cursor()
        try:
            # Aquí puedes agregar la lógica para insertar en una tabla de liquidaciones
            # Por ahora solo retornamos el objeto con id simulado
            
            response = LiquidacionResponse(
                id=1,  # Este sería el ID generado
                **liquidacion.dict()
            )
            response.calcular_total()
            
            return response
        except Exception as e:
            print(e)
            cnx.rollback()
            raise e
        finally:
            cursor.close()
            cnx.close()
