from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Doctor(Base):
    __tablename__ = "doctores"

    id_doctor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    segundo_nombre = Column(String(100), nullable=True)
    especializacion = Column(String(100), nullable=True)
    direccion = Column(String(200), nullable=True)
    estatus = Column(String(50), nullable=True)
    ciudad = Column(String(100), nullable=True)

    # Relaciones
    citas = relationship("Cita", back_populates="doctor", cascade="all, delete")
    horarios = relationship("HorarioDoctor", back_populates="doctor", cascade="all, delete")
