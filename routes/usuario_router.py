from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.usuario_model import Usuario
from schemas.usuario_schema import UsuarioCreateSchema, LoginSchema

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# ---------------------------
# Dependencia DB
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# Crear usuario
# ---------------------------
@router.post("/create")
def crear_usuario(data: UsuarioCreateSchema, db: Session = Depends(get_db)):

    if db.query(Usuario).filter(Usuario.correo == data.correo).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    nuevo = Usuario(
        nombre=data.nombre,
        segundo_nombre=data.segundo_nombre,
        celular=data.celular,
        correo=data.correo,
        rol=data.rol,
        direccion=data.direccion,
        ciudad=data.ciudad,
    )
    nuevo.set_password(data.contrasenia)

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {"message": "Usuario creado", "data": nuevo.to_dict()}

# ---------------------------
# Login
# ---------------------------
@router.post("/login")
def login_usuario(data: LoginSchema, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.correo == data.correo).first()

    if not usuario or not usuario.check_password(data.contrasenia):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {"message": "Login exitoso", "data": usuario.to_dict()}
