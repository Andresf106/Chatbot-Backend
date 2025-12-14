from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.doctor_model import Doctor

router = APIRouter(prefix="/doctores", tags=["Doctores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def listar_doctores(db: Session = Depends(get_db)):
    doctores = db.query(Doctor).all()
    return [d.to_dict() for d in doctores]

@router.get("/{id_doctor}")
def obtener_doctor(id_doctor: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).get(id_doctor)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    return doctor.to_dict()

@router.post("/")
def crear_doctor(data: dict, db: Session = Depends(get_db)):
    nuevo = Doctor(
        nombre=data.get("nombre"),
        especialidad=data.get("especialidad"),
        telefono=data.get("telefono"),
        correo=data.get("correo")
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"message": "Doctor creado", "data": nuevo.to_dict()}

@router.put("/{id_doctor}")
def actualizar_doctor(id_doctor: int, data: dict, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).get(id_doctor)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    for key, value in data.items():
        if hasattr(doctor, key):
            setattr(doctor, key, value)
    db.commit()
    return {"message": "Doctor actualizado correctamente"}

@router.delete("/{id_doctor}")
def eliminar_doctor(id_doctor: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).get(id_doctor)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor eliminado correctamente"}
