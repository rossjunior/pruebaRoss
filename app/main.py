from fastapi import FastAPI
from app.api.zonas.router import router as zonas_router
from app.api.auth.router import router as auth_router
from app.api.departamentos.router import router as departamentos_router
from app.api.tipos_proceso.router import router as tipos_proceso_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(departamentos_router, prefix="/api/departamentos", tags=["departamentos"])
app.include_router(tipos_proceso_router, prefix="/api/tipos_proceso", tags=["tipos_proceso"])
app.include_router(zonas_router, prefix="/zonas-deforestadas", tags=["Zonas"])