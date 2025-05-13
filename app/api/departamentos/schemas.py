from pydantic import BaseModel
from typing import List

class DepartamentoBase(BaseModel):
    nombre: str

class DepartamentoOut(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True

class DepartamentoListResponse(BaseModel):
    total: int
    items: List[DepartamentoOut]
