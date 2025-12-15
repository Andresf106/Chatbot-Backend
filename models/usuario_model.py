from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import Column, Integer, String
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    segundo_nombre = Column(String, nullable=True)
    celular = Column(String, nullable=True)
    gmail = Column(String, nullable=True)  # <- aquí lo hacemos opcional
    contrasena = Column(String, nullable=False)
    rol = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    ciudad = Column(String, nullable=True)
    correo = Column(String, nullable=False)


    citas = relationship("Cita", back_populates="usuario")

    def set_password(self, password: str):
        self.contrasena = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.contrasena, password)
