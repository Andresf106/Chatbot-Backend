from pydantic import BaseModel
from typing import Optional


class CitaBase(BaseModel):
    hora_cita: str
    dia_cita: str
    motivo: str
    estado: Optional[str] = "pendiente"
    id_usuario: int
    id_doctor: int


class CitaCreate(CitaBase):
    pass


class CitaResponse(CitaBase):
    id_cita: int

    model_config = {"from_attributes": True}
