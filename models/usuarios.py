# models/usuarios.py
from core.database import get_connection
from dto.usuario import UsuarioLogin, UsuarioResponse
from typing import Optional

class UsuariosModel:

    @staticmethod
    def authenticate(data: UsuarioLogin) -> Optional[UsuarioResponse]:
        cnx = get_connection()
        if not cnx:
            return None
        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id, email, full_name, img, disabled FROM usuarios WHERE email=%s AND password=%s AND disabled=FALSE",
                (data.email, data.password)
            )
            usuario = cursor.fetchone()
            if usuario:
                return UsuarioResponse(**usuario)
            return None
        finally:
            cursor.close()
            cnx.close()
