# models/liquidacion.py
from core.database import get_connection
from dto.liquidacion import LiquidacionCreate, LiquidacionResponse
from typing import List, Optional
from datetime import datetime

class LiquidacionModel:
    @staticmethod
    def get_by_id(empleado_id: int) -> LiquidacionResponse:
        """GET: Obtiene la liquidación de un empleado específico"""
        cnx = get_connection()
        if not cnx:
            return None
        
        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT 
                    e.id,
                    CONCAT(e.nombres, ' ', e.apellidos) as nombre,
                    e.rut,
                    'Empleado' as cargo,
                    c.id as contrato_id,
                    c.sueldo_base,
                    c.afp_id,
                    c.salud_id,
                    c.afc_id,
                    0 as horas_extras
                FROM empleados e
                JOIN contratos c ON e.id = c.empleado_id
                WHERE e.id = %s
                """,
                (empleado_id,)
            )
            liquidacion = cursor.fetchone()
            
            if not liquidacion:
                return None
                
            response = LiquidacionResponse(**liquidacion)
            response.calcular_total()
            return response
        finally:
            cursor.close()
            cnx.close()

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
                    c.id as contrato_id,
                    c.sueldo_base,
                    c.afp_id,
                    c.salud_id,
                    c.afc_id,
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

    @staticmethod
    def save_liquidacion(liq: LiquidacionResponse, periodo: Optional[int] = None, mes: Optional[int] = None) -> int:
        """Inserta una liquidación en la tabla `liquidaciones` y retorna el id generado."""
        cnx = get_connection()
        if not cnx:
            raise Exception("No se pudo conectar a la base de datos")

        cursor = cnx.cursor()
        try:
            # Determinar periodo y mes por defecto
            now = datetime.now()
            if periodo is None:
                periodo = now.year
            if mes is None:
                mes = now.month

            sql = (
                "INSERT INTO liquidaciones (contrato_id, periodo, mes, sueldo_base, horas_extra, gratificacion, total_imponible, total_descuentos, liquido_a_pagar)"
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )

            contrato_id = getattr(liq, 'contrato_id', None)
            if contrato_id is None:
                raise Exception('Contrato_id no disponible para insertar la liquidación')

            params = (
                contrato_id,
                periodo,
                mes,
                liq.sueldo_base,
                getattr(liq, 'horas_extras_monto', 0.0),
                getattr(liq, 'gratificacion', 0.0),
                getattr(liq, 'total_imponible', 0.0),
                getattr(liq, 'total_descuentos', 0.0),
                getattr(liq, 'liquido', 0.0)
            )

            cursor.execute(sql, params)
            cnx.commit()
            inserted_id = cursor.lastrowid
            return inserted_id
        except Exception:
            cnx.rollback()
            raise
        finally:
            cursor.close()
            cnx.close()
