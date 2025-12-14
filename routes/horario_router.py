from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.horario_model import Horario
from models.horario_doctor_model import HorarioDoctor

router = APIRouter(prefix="/horarios", tags=["Horarios"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Crear un horario general
@router.post("/")
def crear_horario(dia: str, hora_inicio: str, hora_fin: str, db: Session = Depends(get_db)):

    nuevo = Horario(
        dia=dia,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"message": "Horario creado", "data": nuevo}


# Asignar horario a un doctor
@router.post("/asignar")
def asignar_horario(id_doctor: int, id_horario: int, db: Session = Depends(get_db)):

    relacion = HorarioDoctor(
        id_doctor=id_doctor,
        id_horario=id_horario
    )

    db.add(relacion)
    db.commit()
    return {"message": "Horario asignado al doctor"}

@router.get("/doctor/{id_doctor}")
def obtener_horarios_doctor(id_doctor: int, db: Session = Depends(get_db)):

    horarios = db.query(HorarioDoctor).filter(HorarioDoctor.id_doctor == id_doctor).all()

    resultado = []
    for h in horarios:
        resultado.append({
            "id_horario": h.horario.id_horario,
            "dia": h.horario.dia,
            "hora_inicio": h.horario.hora_inicio,
            "hora_fin": h.horario.hora_fin
        })

    return resultado
