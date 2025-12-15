# models/cita_model.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Cita(Base):
    __tablename__ = "citas"

    id_cita = Column(Integer, primary_key=True, index=True)
    hora_cita = Column(String(20))
    dia_cita = Column(String(20))
    motivo = Column(String(200))
    estado = Column(String(50))

    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_doctor = Column(Integer, ForeignKey("doctores.id_doctor"))

   
    usuario = relationship("Usuario", back_populates="citas")
    doctor = relationship("Doctor", back_populates="citas")