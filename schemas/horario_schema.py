from pydantic import BaseModel

class HorarioCreate(BaseModel):
    dia: str
    hora_inicio: str
    hora_fin: str

class HorarioResponse(HorarioCreate):
    id_horario: int

    model_config = {"from_attributes": True}
