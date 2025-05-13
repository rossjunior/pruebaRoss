from pydantic import BaseModel
from typing import List

class TipoProcesoOut(BaseModel):
    id: int
    nombre: str
    class Config:
        orm_mode = True

class DepartamentoOut(BaseModel):
    id: int
    nombre: str
    class Config:
        orm_mode = True

class ZonaBase(BaseModel):
    nombre_zona: str
    tipo_proceso: str
    departamento: str
    geom: str

class ZonaOut(BaseModel):
    id: int
    nombre_zona: str
    tipo_proceso: TipoProcesoOut
    departamento: DepartamentoOut
    class Config:
        orm_mode = True

class ZonaListResponse(BaseModel):
    total: int
    items: List[ZonaOut]