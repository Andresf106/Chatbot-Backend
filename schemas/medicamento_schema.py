from pydantic import BaseModel
from typing import Optional


class MedicamentoBase(BaseModel):
    nombre: str
    dosis: Optional[str] = None
    presentacion: Optional[str] = None
    descripcion: Optional[str] = None


class MedicamentoCreate(MedicamentoBase):
    pass


class MedicamentoResponse(MedicamentoBase):
    id_medicamento: int

    model_config = {"from_attributes": True}
