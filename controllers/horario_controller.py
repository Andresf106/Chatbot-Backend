from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.horario_doctor_model import HorarioDoctor
from models.cita_model import Cita

router = APIRouter()

# ------------------------------
# DEPENDENCIA DE SESSION
# ------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------------------
# CREAR HORARIO PARA UN DOCTOR
# --------------------------------------------------------
@router.post("/")
def crear_horario(data: dict, db: Session = Depends(get_db)):
    horario = HorarioDoctor(
        id_doctor=data["id_doctor"],
        dia_semana=data["dia_semana"],
        hora_inicio=data["hora_inicio"],
        hora_fin=data["hora_fin"]
    )
    db.add(horario)
    db.commit()
    db.refresh(horario)
    return horario.to_dict()

# --------------------------------------------------------
# LISTAR HORARIOS DE UN DOCTOR
# --------------------------------------------------------
@router.get("/doctor/{id_doctor}")
def obtener_horarios(id_doctor: int, db: Session = Depends(get_db)):
    horarios = db.query(HorarioDoctor).filter_by(id_doctor=id_doctor).all()
    return [h.to_dict() for h in horarios]

# --------------------------------------------------------
# DÍAS DISPONIBLES PARA CITAS (SEGÚN HORARIOS)
# --------------------------------------------------------
@router.get("/doctor/{id_doctor}/dias-disponibles")
def obtener_dias_disponibles(id_doctor: int, db: Session = Depends(get_db)):
    horarios = db.query(HorarioDoctor).filter_by(id_doctor=id_doctor).all()

    if not horarios:
        raise HTTPException(status_code=404, detail="El doctor no tiene horarios registrados")

    dias = list({h.dia_semana for h in horarios})

    return {"dias_disponibles": dias}

# --------------------------------------------------------
# HORAS DISPONIBLES PARA UN DÍA ESPECÍFICO
# --------------------------------------------------------
@router.get("/doctor/{id_doctor}/horas-disponibles/{dia_semana}")
def obtener_horas_disponibles(id_doctor: int, dia_semana: str, db: Session = Depends(get_db)):

    horario = (
        db.query(HorarioDoctor)
        .filter_by(id_doctor=id_doctor, dia_semana=dia_semana)
        .first()
    )

    if not horario:
        raise HTTPException(status_code=404, detail="No hay horario registrado para ese día")

    # Obtener horas ya tomadas (citas existentes)
    citas = (
        db.query(Cita)
        .filter(Cita.id_doctor == id_doctor, Cita.dia_cita == dia_semana)
        .all()
    )

    horas_ocupadas = {c.hora_cita for c in citas}

    # Generar horas disponibles
    import datetime
    h_ini = datetime.datetime.strptime(str(horario.hora_inicio), "%H:%M:%S")
    h_fin = datetime.datetime.strptime(str(horario.hora_fin), "%H:%M:%S")

    horas_disponibles = []

    while h_ini < h_fin:
        hora = h_ini.strftime("%H:%M")
        if hora not in horas_ocupadas:
            horas_disponibles.append(hora)

        h_ini += datetime.timedelta(minutes=30)

    return {"horas_disponibles": horas_disponibles}
