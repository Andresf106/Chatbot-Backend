from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.cita_model import Cita
from schemas.cita_schema import CitaCreate, CitaResponse

router = APIRouter(prefix="/citas", tags=["Citas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------
# LISTAR TODAS LAS CITAS
# ------------------------
@router.get("/", response_model=list[CitaResponse])
def listar_citas(db: Session = Depends(get_db)):
    return db.query(Cita).all()


# ------------------------
# OBTENER CITA POR ID
# ------------------------
@router.get("/{id_cita}", response_model=CitaResponse)
def obtener_cita(id_cita: int, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita


# ------------------------
# CREAR CITA
# ------------------------
@router.post("/", response_model=CitaResponse)
def crear_cita(data: CitaCreate, db: Session = Depends(get_db)):
    nueva_cita = Cita(**data.model_dump())
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita


# ------------------------
# ACTUALIZAR CITA
# ------------------------
@router.put("/{id_cita}", response_model=CitaResponse)
def actualizar_cita(id_cita: int, data: CitaCreate, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    for key, value in data.model_dump().items():
        if hasattr(cita, key):
            setattr(cita, key, value)

    db.commit()
    db.refresh(cita)
    return cita


# ------------------------
# ELIMINAR CITA
# ------------------------
@router.delete("/{id_cita}")
def eliminar_cita(id_cita: int, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    db.delete(cita)
    db.commit()
    return {"message": "Cita eliminada correctamente"}
