from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.db.database import get_db
from app.models import models
from app.api.tipos_proceso.schemas import TipoProcesoBase, TipoProcesoOut, TipoProcesoListResponse
from app.core.security import JWTBearer

router = APIRouter()

@router.get("/", response_model=TipoProcesoListResponse, dependencies=[Depends(JWTBearer())])
def listar_tipos_proceso(skip: int = 0, limit: int = 10, order_by: str = "id",
                         order_dir: str = "asc", db: Session = Depends(get_db)):
    query = db.query(models.TipoProceso)

    total = query.count()

    order_attr = getattr(models.TipoProceso, order_by, None)
    if order_attr:
        direction = desc(order_attr) if order_dir == "desc" else asc(order_attr)
        query = query.order_by(direction)

    items = query.offset(skip).limit(limit).all()
    return {"total": total, "items": items}

@router.post("/", response_model=TipoProcesoOut, dependencies=[Depends(JWTBearer())])
def crear_tipo_proceso(tipo_proceso: TipoProcesoBase, db: Session = Depends(get_db)):
    try:
        # Check if tipo_proceso already exists
        existing = db.query(models.TipoProceso).filter_by(nombre=tipo_proceso.nombre).first()
        if existing:
            raise HTTPException(status_code=400, detail="Tipo de proceso ya existe")

        tipo_proceso_db = models.TipoProceso(nombre=tipo_proceso.nombre)
        db.add(tipo_proceso_db)
        db.commit()
        db.refresh(tipo_proceso_db)
        return tipo_proceso_db

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tipo_proceso_id}", response_model=TipoProcesoOut, dependencies=[Depends(JWTBearer())])
def obtener_tipo_proceso(tipo_proceso_id: int, db: Session = Depends(get_db)):
    tipo_proceso = db.query(models.TipoProceso).filter_by(id=tipo_proceso_id).first()
    if not tipo_proceso:
        raise HTTPException(status_code=404, detail="Tipo de proceso no encontrado")
    return tipo_proceso

@router.put("/{tipo_proceso_id}", response_model=TipoProcesoOut, dependencies=[Depends(JWTBearer())])
def actualizar_tipo_proceso(tipo_proceso_id: int, tipo_proceso: TipoProcesoBase, db: Session = Depends(get_db)):
    tipo_proceso_db = db.query(models.TipoProceso).filter_by(id=tipo_proceso_id).first()
    if not tipo_proceso_db:
        raise HTTPException(status_code=404, detail="Tipo de proceso no encontrado")

    try:
        # Check if new name already exists for another tipo_proceso
        existing = db.query(models.TipoProceso).filter_by(nombre=tipo_proceso.nombre).first()
        if existing and existing.id != tipo_proceso_id:
            raise HTTPException(status_code=400, detail="Ya existe un tipo de proceso con ese nombre")

        tipo_proceso_db.nombre = tipo_proceso.nombre
        db.commit()
        db.refresh(tipo_proceso_db)
        return tipo_proceso_db

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{tipo_proceso_id}", dependencies=[Depends(JWTBearer())])
def eliminar_tipo_proceso(tipo_proceso_id: int, db: Session = Depends(get_db)):
    tipo_proceso = db.query(models.TipoProceso).filter_by(id=tipo_proceso_id).first()
    if not tipo_proceso:
        raise HTTPException(status_code=404, detail="Tipo de proceso no encontrado")

    # Check if tipo_proceso is being used in zonas
    zonas = db.query(models.ZonaDeforestada).filter_by(tipo_proceso_id=tipo_proceso_id).first()
    if zonas:
        raise HTTPException(status_code=400,
                           detail="No se puede eliminar el tipo de proceso porque está siendo usado en zonas deforestadas")

    db.delete(tipo_proceso)
    db.commit()
    return {"ok": True, "message": "Tipo de proceso eliminado correctamente"}
