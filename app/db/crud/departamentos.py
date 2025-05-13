from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from shapely import wkt
from app.models import models
from app.api.zonas import schemas
from shapely.errors import WKTReadingError
from sqlalchemy import asc, desc


def get_or_create_departamento(db: Session, nombre: str):
    depto = db.query(models.Departamento).filter_by(nombre=nombre).first()
    if not depto:
        depto = models.Departamento(nombre=nombre)
        db.add(depto)
        db.commit()
        db.refresh(depto)
    return depto
