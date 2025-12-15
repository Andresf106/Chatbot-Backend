from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.doctor_model import Doctor
from schemas.doctor_schema import DoctorCreate, DoctorResponse

router = APIRouter(prefix="/doctores", tags=["Doctores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DoctorResponse)
def crear_doctor(data: DoctorCreate, db: Session = Depends(get_db)):
    doctor = Doctor(**data.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor

@router.get("/", response_model=list[DoctorResponse])
def listar_doctores(db: Session = Depends(get_db)):
    return db.query(Doctor).all()

@router.get("/{id_doctor}", response_model=DoctorResponse)
def obtener_doctor(id_doctor: int, db: Session = Depends(get_db)):
    doctor = db.get(Doctor, id_doctor)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    return doctor

@router.delete("/{id_doctor}")
def eliminar_doctor(id_doctor: int, db: Session = Depends(get_db)):
    doctor = db.get(Doctor, id_doctor)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor eliminado"}
