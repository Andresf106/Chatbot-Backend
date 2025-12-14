# controllers/login_controller.py
from fastapi import APIRouter, HTTPException
from schemas.usuario_schema import LoginSchema
from models.usuario_model import Usuario
from database import SessionLocal

router = APIRouter()
db = SessionLocal()

@router.post("/login")
def login(data: LoginSchema):
    user = db.query(Usuario).filter(Usuario.gmail == data.gmail).first()

    if not user or user.contrasenia != data.contrasenia:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {
        "id": user.id,
        "nombre": user.nombre,
        "gmail": user.gmail,
        "rol": user.rol
    }
