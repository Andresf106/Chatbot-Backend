# routes/usuario_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.usuario_model import Usuario
from schemas.usuario_schema import UsuarioCreateSchema, LoginSchema

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/")
def crear_usuario(data: UsuarioCreateSchema, db: Session = Depends(get_db)):

    if db.query(Usuario).filter(Usuario.correo == data.correo).first():
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    nuevo = Usuario(
        nombre=data.nombre,
        segundo_nombre=data.segundo_nombre,
        celular=data.celular,
        gmail=data.gmail,  # ahora opcional
        rol=data.rol,
        direccion=data.direccion,
        ciudad=data.ciudad,
        correo=data.correo
    )
    nuevo.set_password(data.contrasena)

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {"message": "Usuario creado correctamente", "id_usuario": nuevo.id_usuario}

@router.post("/login")
def login_usuario(data: LoginSchema, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(
        Usuario.correo == data.correo
    ).first()

    if not usuario or not usuario.check_password(data.contrasena):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return usuario.to_dict()
