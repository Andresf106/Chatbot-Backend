from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

from .usuario_medicamento_model import UsuarioMedicamento

class Medicamento(Base):
    __tablename__ = "medicamentos"

    id_medicamento = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    dosis = Column(String(100))
    presentacion = Column(String(100))
    descripcion = Column(String(255))

    usuarios = relationship(
        UsuarioMedicamento,
        back_populates="medicamento"
    )
