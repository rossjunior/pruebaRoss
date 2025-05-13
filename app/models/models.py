from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.db.database import Base

class Departamento(Base):
    __tablename__ = "departamentos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)

class TipoProceso(Base):
    __tablename__ = "tipos_proceso"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)

class ZonaDeforestada(Base):
    __tablename__ = "zonas_deforestadas"
    id = Column(Integer, primary_key=True, index=True)
    nombre_zona = Column(String, nullable=False)
    tipo_proceso_id = Column(Integer, ForeignKey("tipos_proceso.id"))
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))
    geometry = Column(Geometry(geometry_type='POLYGON', srid=3116), nullable=False)

    tipo_proceso = relationship("TipoProceso")
    departamento = relationship("Departamento")
