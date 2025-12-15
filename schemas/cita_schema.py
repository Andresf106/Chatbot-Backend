from pydantic import BaseModel

# Para crear una cita
class CitaCreate(BaseModel):
    hora_cita: str
    dia_cita: str
    motivo: str
    estado: str = "Pendiente"
    id_usuario: int
    id_doctor: int

# Para respuesta
class CitaResponse(BaseModel):
    id_cita: int
    hora_cita: str
    dia_cita: str
    motivo: str
    estado: str
    id_usuario: int
    id_doctor: int

    class Config:
        orm_mode = True
