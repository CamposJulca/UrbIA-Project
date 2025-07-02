# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import router as api_router

app = FastAPI(
    title="UrbIA API",
    description="API backend para monitoreo urbano inteligente con ThingsBoard",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o usa ["http://localhost:8000"] para mayor seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir rutas del API
app.include_router(api_router, prefix="/api")

# Ruta básica sin prefijo, útil para prueba rápida desde CLI
@app.get("/ping", tags=["Sistema"])
async def ping():
    return {"message": "UrbIA API operativa 🟢"}
