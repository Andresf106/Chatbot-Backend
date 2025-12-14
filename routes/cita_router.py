from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models.cita_model import Cita
from models.horario_doctor_model import HorarioDoctor
from models.horario_model import Horario

router = APIRouter(prefix="/citas", tags=["Citas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear cita validando horario
@router.post("/")
def crear_cita(id_usuario: int, id_doctor: int, dia: str, hora: str, motivo: str, db: Session = Depends(get_db)):

    # 1️⃣ Obtener horarios asignados al doctor
    horarios_doctor = (
        db.query(HorarioDoctor)
        .filter(HorarioDoctor.id_doctor == id_doctor)
        .all()
    )

    if not horarios_doctor:
        raise HTTPException(status_code=400, detail="El doctor no tiene horarios asignados")

    # 2️⃣ Verificar si la hora/día está dentro de un horario
    permitido = False
    for h in horarios_doctor:
        horario = h.horario

        if horario.dia == dia:
            if horario.hora_inicio <= hora <= horario.hora_fin:
                permitido = True
                break

    if not permitido:
        raise HTTPException(
            status_code=400,
            detail="El horario solicitado no está dentro del horario del doctor"
        )

    # 3️⃣ Verificar que la hora no esté ocupada ya
    cita_existente = (
        db.query(Cita)
        .filter(
            Cita.id_doctor == id_doctor,
            Cita.dia_cita == dia,
            Cita.hora_cita == hora
        )
        .first()
    )

    if cita_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una cita en ese horario"
        )

    # 4️⃣ Crear cita
    nueva_cita = Cita(
        id_usuario=id_usuario,
        id_doctor=id_doctor,
        dia_cita=dia,
        hora_cita=hora,
        motivo=motivo
    )

    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)

    return {
        "message": "Cita agendada correctamente",
        "data": {
            "id_cita": nueva_cita.id_cita,
            "dia": dia,
            "hora": hora
        }
    }
