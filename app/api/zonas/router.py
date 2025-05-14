from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from shapely import wkt
from geoalchemy2.shape import from_shape

from app.api.departamentos.schemas import DepartamentoOut
from app.api.tipos_proceso.schemas import TipoProcesoOut
from app.db.database import get_db
from app.models import models
from app.api.zonas.schemas import ZonaBase, ZonaOut, ZonaListResponse
from app.core.security import JWTBearer
from sqlalchemy import desc, asc, func
import json

router = APIRouter()

@router.get("/", response_model=ZonaListResponse, dependencies=[Depends(JWTBearer())])
def listar_zonas(
    tipo_proceso: str = None,
    departamento: str = None,
    skip: int = 0,
    limit: int = 10,
    order_by: str = "id",
    order_dir: str = "asc",
    db: Session = Depends(get_db)
):
    query = db.query(models.ZonaDeforestada).options(
        joinedload(models.ZonaDeforestada.tipo_proceso),
        joinedload(models.ZonaDeforestada.departamento)
    )

    if tipo_proceso:
        query = query.join(models.TipoProceso).filter(models.TipoProceso.nombre == tipo_proceso)
    if departamento:
        query = query.join(models.Departamento).filter(models.Departamento.nombre == departamento)

    total = query.count()

    # Ordenamiento dinámico
    order_attr = getattr(models.ZonaDeforestada, order_by, None)
    if order_attr:
        direction = desc(order_attr) if order_dir == "desc" else asc(order_attr)
        query = query.order_by(direction)

    zonas = query.offset(skip).limit(limit).all()

    # Convertir geometría a GeoJSON
    items = []
    for zona in zonas:
        geom_geojson = db.scalar(func.ST_AsGeoJSON(zona.geometry))
        zona_out = ZonaOut(
            id=zona.id,
            nombre_zona=zona.nombre_zona,
            geom=json.loads(geom_geojson),
            tipo_proceso=TipoProcesoOut(
                id=zona.tipo_proceso.id,
                nombre=zona.tipo_proceso.nombre
            ).model_dump(),
            departamento=DepartamentoOut(
                id=zona.departamento.id,
                nombre=zona.departamento.nombre
            ).model_dump()
        )
        items.append(zona_out)

    return {"total": total, "items": items}


@router.post("/", response_model=ZonaOut, dependencies=[Depends(JWTBearer())])
def crear_zona(zona: ZonaBase, db: Session = Depends(get_db)):
    try:
        geom_shape = wkt.loads(zona.geom)
        if not geom_shape.is_valid or geom_shape.geom_type != "Polygon":
            raise ValueError("Geometría no válida. Debe ser un POLYGON.")
        geom = from_shape(geom_shape, srid=3116)

        tipo = db.query(models.TipoProceso).filter_by(nombre=zona.tipo_proceso).first()
        if not tipo:
            raise ValueError("Tipo de proceso no existe")

        depto = db.query(models.Departamento).filter_by(nombre=zona.departamento).first()
        if not depto:
            raise ValueError("Departamento no existe")

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

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{zona_id}", response_model=ZonaOut, dependencies=[Depends(JWTBearer())])
def obtener_zona(zona_id: int, db: Session = Depends(get_db)):
    zona = db.query(models.ZonaDeforestada).filter_by(id=zona_id).first()

    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")

    geom_geojson = db.scalar(func.ST_AsGeoJSON(zona.geometry))
    zona.geom = json.loads(geom_geojson)

    return zona

@router.put("/{zona_id}", response_model=ZonaOut, dependencies=[Depends(JWTBearer())])
def actualizar_zona(zona_id: int, zona: ZonaBase, db: Session = Depends(get_db)):
    zona_db = db.query(models.ZonaDeforestada).filter_by(id=zona_id).first()
    if not zona_db:
        raise HTTPException(status_code=404, detail="Zona no encontrada")

    try:
        geom_shape = wkt.loads(zona.geom)
        if not geom_shape.is_valid or geom_shape.geom_type != "Polygon":
            raise ValueError("Geometría no válida. Debe ser un POLYGON.")
        geom = from_shape(geom_shape, srid=3116)

        tipo = db.query(models.TipoProceso).filter_by(nombre=zona.tipo_proceso).first()
        if not tipo:
            raise ValueError("Tipo de proceso no existe")

        depto = db.query(models.Departamento).filter_by(nombre=zona.departamento).first()
        if not depto:
            raise ValueError("Departamento no existe")

        zona_db.nombre_zona = zona.nombre_zona
        zona_db.tipo_proceso_id = tipo.id
        zona_db.departamento_id = depto.id
        zona_db.geometry = geom

        db.commit()
        db.refresh(zona_db)
        return zona_db

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{zona_id}", dependencies=[Depends(JWTBearer())])
def eliminar_zona(zona_id: int, db: Session = Depends(get_db)):
    zona = db.query(models.ZonaDeforestada).filter_by(id=zona_id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    db.delete(zona)
    db.commit()
    return {"ok": True, "message": "Zona eliminada correctamente"}
