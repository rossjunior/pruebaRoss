from pydantic import BaseModel
from typing import List

class TipoProcesoBase(BaseModel):
    nombre: str

class TipoProcesoOut(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True

class TipoProcesoListResponse(BaseModel):
    total: int
    items: List[TipoProcesoOut]
