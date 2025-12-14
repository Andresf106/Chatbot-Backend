from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class UsuarioMedicamento(Base):
    __tablename__ = "usuario_medicamentos"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_medicamento = Column(Integer, ForeignKey("medicamentos.id_medicamento"))

    usuario = relationship("Usuario", back_populates="medicamentos")
    medicamento = relationship("Medicamento", back_populates="usuarios")
