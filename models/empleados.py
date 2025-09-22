from core.database import get_connection

class EmpleadosModel:
    @staticmethod
    def get_all():
        cnx = get_connection()
        if not cnx:
            return []
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT id, nombres, apellidos, rut, fecha_nacimiento, direccion FROM empleados")
        empleados = cursor.fetchall()
        cursor.close()
        cnx.close()
        return empleados

    @staticmethod
    def create(
        nombres, apellidos, rut, fecha_nacimiento, direccion,
        empresa_id, tipo_contrato, fecha_inicio, fecha_termino,
        sueldo_base, afp_id, salud_id, afc_id
    ):
        cnx = get_connection()
        if not cnx:
            return False
        cursor = cnx.cursor()
        try:
            # Insertar empleado
            sql_empleado = """
            INSERT INTO empleados (nombres, apellidos, rut, fecha_nacimiento, direccion)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_empleado, (nombres, apellidos, rut, fecha_nacimiento, direccion))
            empleado_id = cursor.lastrowid

            # Insertar contrato
            sql_contrato = """
            INSERT INTO contratos (
                empleado_id, empresa_id, tipo, fecha_inicio, fecha_termino, sueldo_base, afp_id, salud_id, afc_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_contrato, (
                empleado_id, empresa_id, tipo_contrato, fecha_inicio,
                fecha_termino, sueldo_base, afp_id, salud_id, afc_id
            ))

            cnx.commit()
            return empleado_id

        except Exception as e:
            cnx.rollback()
            raise e

        finally:
            cursor.close()
            cnx.close()