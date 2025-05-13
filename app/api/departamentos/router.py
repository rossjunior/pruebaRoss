from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.db.database import get_db
from app.models import models
from app.api.departamentos.schemas import DepartamentoBase, DepartamentoOut, DepartamentoListResponse
from app.core.security import JWTBearer

router = APIRouter()

@router.get("/", response_model=DepartamentoListResponse, dependencies=[Depends(JWTBearer())])
def listar_departamentos(skip: int = 0, limit: int = 10, order_by: str = "id",
                          order_dir: str = "asc", db: Session = Depends(get_db)):
    query = db.query(models.Departamento)

    total = query.count()

    order_attr = getattr(models.Departamento, order_by, None)
    if order_attr:
        direction = desc(order_attr) if order_dir == "desc" else asc(order_attr)
        query = query.order_by(direction)

    items = query.offset(skip).limit(limit).all()
    return {"total": total, "items": items}

@router.post("/", response_model=DepartamentoOut, dependencies=[Depends(JWTBearer())])
def crear_departamento(departamento: DepartamentoBase, db: Session = Depends(get_db)):
    try:
        # Check if departamento already exists
        existing = db.query(models.Departamento).filter_by(nombre=departamento.nombre).first()
        if existing:
            raise HTTPException(status_code=400, detail="Departamento ya existe")

        departamento_db = models.Departamento(nombre=departamento.nombre)
        db.add(departamento_db)
        db.commit()
        db.refresh(departamento_db)
        return departamento_db

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{departamento_id}", response_model=DepartamentoOut, dependencies=[Depends(JWTBearer())])
def obtener_departamento(departamento_id: int, db: Session = Depends(get_db)):
    departamento = db.query(models.Departamento).filter_by(id=departamento_id).first()
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    return departamento

@router.put("/{departamento_id}", response_model=DepartamentoOut, dependencies=[Depends(JWTBearer())])
def actualizar_departamento(departamento_id: int, departamento: DepartamentoBase, db: Session = Depends(get_db)):
    departamento_db = db.query(models.Departamento).filter_by(id=departamento_id).first()
    if not departamento_db:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")

    try:
        # Check if new name already exists for another departamento
        existing = db.query(models.Departamento).filter_by(nombre=departamento.nombre).first()
        if existing and existing.id != departamento_id:
            raise HTTPException(status_code=400, detail="Ya existe un departamento con ese nombre")

        departamento_db.nombre = departamento.nombre
        db.commit()
        db.refresh(departamento_db)
        return departamento_db

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{departamento_id}", dependencies=[Depends(JWTBearer())])
def eliminar_departamento(departamento_id: int, db: Session = Depends(get_db)):
    departamento = db.query(models.Departamento).filter_by(id=departamento_id).first()
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")

    # Check if departamento is being used in zonas
    zonas = db.query(models.ZonaDeforestada).filter_by(departamento_id=departamento_id).first()
    if zonas:
        raise HTTPException(status_code=400,
                           detail="No se puede eliminar el departamento porque está siendo usado en zonas deforestadas")

    db.delete(departamento)
    db.commit()
    return {"ok": True, "message": "Departamento eliminado correctamente"}
