from pydantic import BaseModel

class UsuarioCreateSchema(BaseModel):
    nombre: str
    segundo_nombre: str | None = None
    celular: str | None = None
    correo: str
    rol: str | None = None
    direccion: str | None = None
    ciudad: str | None = None
    contrasenia: str


class LoginSchema(BaseModel):
    correo: str
    contrasenia: str
