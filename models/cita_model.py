from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Cita(Base):
    __tablename__ = "citas"

    id_cita = Column(Integer, primary_key=True, index=True)
    hora_cita = Column(String(10), nullable=False)
    dia_cita = Column(String(20), nullable=False)
    motivo = Column(String(255), nullable=True)
    estado = Column(String(20), default="Pendiente")

    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_doctor = Column(Integer, ForeignKey("doctores.id_doctor"))

    usuario = relationship("Usuario", back_populates="citas")
    doctor = relationship("Doctor", back_populates="citas")
