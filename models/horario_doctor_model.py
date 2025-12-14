from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class HorarioDoctor(Base):
    __tablename__ = "horarios_doctores"

    id = Column(Integer, primary_key=True, index=True)

    id_doctor = Column(Integer, ForeignKey("doctores.id_doctor"), nullable=False)
    id_horario = Column(Integer, ForeignKey("horarios.id_horario"), nullable=False)

    # Relaciones hacia Doctor y Horario
    doctor = relationship("Doctor", back_populates="horarios")
    horario = relationship("Horario", back_populates="doctores")
