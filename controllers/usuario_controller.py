from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.usuario_model import Usuario
from pydantic import BaseModel

router = APIRouter()

# ---------------------------
# Schemas
# ---------------------------
class UsuarioCreateSchema(BaseModel):
    nombre: str
    correo: str
    contrasenia: str

class LoginSchema(BaseModel):
    correo: str
    contrasenia: str

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
# Rutas
# ---------------------------

# Crear usuario
@router.post("/")
def crear_usuario(data: UsuarioCreateSchema, db: Session = Depends(get_db)):

    if db.query(Usuario).filter(Usuario.correo == data.correo).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    nuevo = Usuario(
        nombre=data.nombre,
        correo=data.correo
    )
    nuevo.set_password(data.contrasenia)

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"message": "Usuario creado", "data": nuevo.to_dict()}


# Login
@router.post("/login")
def login_usuario(data: LoginSchema, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.correo == data.correo).first()

    if not usuario or not usuario.check_password(data.contrasenia):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {"message": "Login exitoso", "data": usuario.to_dict()}


# Listar usuarios
@router.get("/")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return [u.to_dict() for u in usuarios]


# Obtener usuario por id
@router.get("/{id_usuario}")
def obtener_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).get(id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario.to_dict()


# Actualizar usuario
@router.put("/{id_usuario}")
def actualizar_usuario(id_usuario: int, data: UsuarioCreateSchema, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).get(id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if data.contrasenia:
        usuario.set_password(data.contrasenia)

    usuario.nombre = data.nombre
    usuario.correo = data.correo

    db.commit()
    return {"message": "Usuario actualizado correctamente"}


# Eliminar usuario
@router.delete("/{id_usuario}")
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).get(id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}
