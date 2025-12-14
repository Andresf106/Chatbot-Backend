from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Horario(Base):
    __tablename__ = "horarios"

    id_horario = Column(Integer, primary_key=True, index=True)
    dia = Column(String(20), nullable=False)
    hora_inicio = Column(String(10), nullable=False)
    hora_fin = Column(String(10), nullable=False)

    # Relación inversa con la tabla intermedia
    doctores = relationship("HorarioDoctor", back_populates="horario")
