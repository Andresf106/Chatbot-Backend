from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Doctor(Base):
    __tablename__ = "doctores"

    id_doctor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    segundo_nombre = Column(String(100))
    especializacion = Column(String(120))
    direccion = Column(String(200))
    estatus = Column(String(50))
    ciudad = Column(String(100))

    # Relaciones
    citas = relationship("Cita", back_populates="doctor")
    horarios = relationship("HorarioDoctor", back_populates="doctor")