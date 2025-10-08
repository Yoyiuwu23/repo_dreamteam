# dto/usuario.py
from pydantic import BaseModel
from typing import Optional

class UsuarioLogin(BaseModel):
    email: str
    password: str

class UsuarioResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    img: Optional[str] = None
    disabled: bool
