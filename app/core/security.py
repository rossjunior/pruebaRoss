from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 60

def crear_token(usuario: str):
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    return jwt.encode({"sub": usuario, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        return None

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            usuario = verificar_token(credentials.credentials)
            if usuario is None:
                raise HTTPException(status_code=403, detail="Token inválido")
            return usuario
        raise HTTPException(status_code=403, detail="Token requerido")
