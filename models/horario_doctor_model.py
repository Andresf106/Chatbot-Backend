from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class HorarioDoctor(Base):
    __tablename__ = "horario_doctor"

    id = Column(Integer, primary_key=True, index=True)
    id_doctor = Column(Integer, ForeignKey("doctores.id_doctor"), nullable=False)
    id_horario = Column(Integer, ForeignKey("horarios.id_horario"), nullable=False)

    doctor = relationship("Doctor", back_populates="horarios")
    horario = relationship("Horario", back_populates="doctores")
