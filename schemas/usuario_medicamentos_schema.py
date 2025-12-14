from pydantic import BaseModel


class UsuarioMedicamentoBase(BaseModel):
    id_usuario: int
    id_medicamentos: int


class UsuarioMedicamentoCreate(UsuarioMedicamentoBase):
    pass


class UsuarioMedicamentoResponse(UsuarioMedicamentoBase):
    id: int

    model_config = {"from_attributes": True}
