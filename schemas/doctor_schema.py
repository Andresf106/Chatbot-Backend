from pydantic import BaseModel
from typing import Optional


class DoctorBase(BaseModel):
    nombre: str
    segundo_nombre: Optional[str] = None
    especializacion: Optional[str] = None
    direccion: Optional[str] = None
    horario: Optional[str] = None
    estatus: Optional[str] = None
    ciudad: Optional[str] = None


class DoctorCreate(DoctorBase):
    pass


class DoctorResponse(DoctorBase):
    id_doctor: int

    model_config = {"from_attributes": True}
