# schemas/usuario_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioCreateSchema(BaseModel):
    nombre: str
    segundo_nombre: Optional[str] = None
    celular: Optional[str] = None
    gmail: Optional[str] = None  # <- agregar esto
    contrasena: str
    rol: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    correo: EmailStr

class LoginSchema(BaseModel):
    correo: EmailStr
    contrasena: str
