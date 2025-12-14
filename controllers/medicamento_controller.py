from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.medicamento_model import Medicamento

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def listar_medicamentos(db: Session = Depends(get_db)):
    medicamentos = db.query(Medicamento).all()
    return [m.__dict__ for m in medicamentos]

@router.get("/{id_medicamento}")
def obtener_medicamento(id_medicamento: int, db: Session = Depends(get_db)):
    medicamento = db.query(Medicamento).get(id_medicamento)
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado")
    return medicamento.__dict__

@router.post("/")
def crear_medicamento(data: dict, db: Session = Depends(get_db)):
    nuevo = Medicamento(
        nombre=data.get("nombre"),
        dosis=data.get("dosis"),
        presentacion=data.get("presentacion"),
        descripcion=data.get("descripcion")
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"message": "Medicamento creado", "data": nuevo.__dict__}

@router.put("/{id_medicamento}")
def actualizar_medicamento(id_medicamento: int, data: dict, db: Session = Depends(get_db)):
    medicamento = db.query(Medicamento).get(id_medicamento)
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado")

    for key, value in data.items():
        if hasattr(medicamento, key):
            setattr(medicamento, key, value)

    db.commit()
    return {"message": "Medicamento actualizado correctamente"}

@router.delete("/{id_medicamento}")
def eliminar_medicamento(id_medicamento: int, db: Session = Depends(get_db)):
    medicamento = db.query(Medicamento).get(id_medicamento)
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado")

    db.delete(medicamento)
    db.commit()
    return {"message": "Medicamento eliminado correctamente"}
