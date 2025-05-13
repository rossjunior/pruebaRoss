from sqlalchemy.orm import Session
from app.models import models

def get_or_create_tipo_proceso(db: Session, nombre: str):
    tipo = db.query(models.TipoProceso).filter_by(nombre=nombre).first()
    if not tipo:
        tipo = models.TipoProceso(nombre=nombre)
        db.add(tipo)
        db.commit()
        db.refresh(tipo)
    return tipo
