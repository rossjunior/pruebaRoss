from fastapi import FastAPI
from app.api.zonas.router import router as zonas_router
from app.api.auth.router import router as auth_router

app = FastAPI()

app.include_router(zonas_router, prefix="/zonas-deforestadas", tags=["Zonas"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])