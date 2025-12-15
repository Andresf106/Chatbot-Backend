from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.horario_model import Horario
from models.horario_doctor_model import HorarioDoctor
from schemas.horario_schema import HorarioCreate, HorarioResponse

router = APIRouter(prefix="/horarios", tags=["Horarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear horario
@router.post("/", response_model=HorarioResponse)
def crear_horario(data: HorarioCreate, db: Session = Depends(get_db)):
    horario = Horario(**data.model_dump())
    db.add(horario)
    db.commit()
    db.refresh(horario)
    return horario

# Asignar horario a doctor
@router.post("/asignar")
def asignar_horario(id_doctor: int, id_horario: int, db: Session = Depends(get_db)):
    relacion = HorarioDoctor(
        id_doctor=id_doctor,
        id_horario=id_horario
    )
    db.add(relacion)
    db.commit()
    return {"message": "Horario asignado correctamente"}

# Obtener horarios de un doctor
@router.get("/doctor/{id_doctor}")
def obtener_horarios_doctor(id_doctor: int, db: Session = Depends(get_db)):
    relaciones = db.query(HorarioDoctor).filter(
        HorarioDoctor.id_doctor == id_doctor
    ).all()

    return [
        {
            "id_horario": r.horario.id_horario,
            "dia": r.horario.dia,
            "hora_inicio": r.horario.hora_inicio,
            "hora_fin": r.horario.hora_fin
        }
        for r in relaciones
    ]
