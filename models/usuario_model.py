from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    segundo_nombre = Column(String(100), nullable=True)
    celular = Column(String(20), nullable=True)
    correo = Column(String(100), unique=True, nullable=False)
    contrasenia = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=True)
    direccion = Column(String(200), nullable=True)
    ciudad = Column(String(100), nullable=True)

    # ❌ Comentamos temporalmente esta relación para evitar el error 500
    # medicamentos = relationship("UsuarioMedicamento", back_populates="usuario")

    citas = relationship("Cita", back_populates="usuario")

    def set_password(self, password: str):
        self.contrasenia = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.contrasenia, password)

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "segundo_nombre": self.segundo_nombre,
            "correo": self.correo,
            "rol": self.rol,
            "ciudad": self.ciudad,
            "celular": self.celular,
            "direccion": self.direccion
        }
