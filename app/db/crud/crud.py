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

def get_or_create_tipo_proceso(db: Session, nombre: str):
    tipo = db.query(models.TipoProceso).filter_by(nombre=nombre).first()
    if not tipo:
        tipo = models.TipoProceso(nombre=nombre)
        db.add(tipo)
        db.commit()
        db.refresh(tipo)
    return tipo


def create_zona(db: Session, zona: schemas.ZonaBase):
    try:
        geom_shape = wkt.loads(zona.geom)
        if not geom_shape.is_valid or geom_shape.geom_type != "Polygon":
            raise ValueError("Geometría no válida. Debe ser un POLYGON válido.")

        geom = from_shape(geom_shape, srid=3116)

        tipo = db.query(models.TipoProceso).filter_by(nombre=zona.tipo_proceso).first()
        if not tipo:
            raise ValueError(f"Tipo de proceso '{zona.tipo_proceso}' no existe.")

        depto = db.query(models.Departamento).filter_by(nombre=zona.departamento).first()
        if not depto:
            raise ValueError(f"Departamento '{zona.departamento}' no existe.")

        zona_db = models.ZonaDeforestada(
            nombre_zona=zona.nombre_zona,
            tipo_proceso_id=tipo.id,
            departamento_id=depto.id,
            geometry=geom
        )
        db.add(zona_db)
        db.commit()
        db.refresh(zona_db)
        return zona_db

    except WKTReadingError:
        raise ValueError("Geometría inválida. Asegúrate de que el campo 'geom' esté en formato WKT válido.")


def get_zonas(db: Session, tipo_proceso=None, departamento=None, skip=0, limit=10, order_by="id", order_dir="asc"):
    query = db.query(models.ZonaDeforestada)

    if tipo_proceso:
        query = query.join(models.TipoProceso).filter(models.TipoProceso.nombre == tipo_proceso)
    if departamento:
        query = query.join(models.Departamento).filter(models.Departamento.nombre == departamento)

    total = query.count()

    order_attr = getattr(models.ZonaDeforestada, order_by, None)
    if order_attr:
        direction = desc(order_attr) if order_dir == "desc" else asc(order_attr)
        query = query.order_by(direction)

    items = query.offset(skip).limit(limit).all()
    return total, items

def get_zona(db: Session, zona_id: int):
    return db.query(models.ZonaDeforestada).filter_by(id=zona_id).first()

def delete_zona(db: Session, zona_id: int):
    zona = get_zona(db, zona_id)
    if zona:
        db.delete(zona)
        db.commit()
        return True
    return False

def update_zona(db: Session, zona_id: int, zona: schemas.ZonaBase):
    zona_db = get_zona(db, zona_id)
    if not zona_db:
        return None

    try:
        geom_shape = wkt.loads(zona.geom)
        if not geom_shape.is_valid or geom_shape.geom_type != "Polygon":
            raise ValueError("Geometría no válida. Debe ser un POLYGON válido.")

        geom = from_shape(geom_shape, srid=3116)

        tipo = db.query(models.TipoProceso).filter_by(nombre=zona.tipo_proceso).first()
        if not tipo:
            raise ValueError(f"Tipo de proceso '{zona.tipo_proceso}' no existe.")

        depto = db.query(models.Departamento).filter_by(nombre=zona.departamento).first()
        if not depto:
            raise ValueError(f"Departamento '{zona.departamento}' no existe.")

        zona_db.nombre_zona = zona.nombre_zona
        zona_db.tipo_proceso_id = tipo.id
        zona_db.departamento_id = depto.id
        zona_db.geometry = geom

        db.commit()
        db.refresh(zona_db)
        return zona_db

    except WKTReadingError:
        raise ValueError("Geometría inválida. Asegúrate de que el campo 'geom' esté en formato WKT válido.")

