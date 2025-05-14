from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.core.security import crear_token

router = APIRouter()
class LoginData(BaseModel):
    username: str
    password: str  # Por ahora sin hash (solo pruebas)

@router.post("/login")
def login(data: LoginData):
    # Validación simple (puedes conectar con base de datos luego)
    if data.username == "admin" and data.password == "admin123":
        token = crear_token(data.username)
        return {"access_token": token}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
