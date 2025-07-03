# Punto de entrada FastAPI

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import inicializar_bd
from app.routes import router as edge_router

# Inicializar la base de datos (crea tablas si no existen)
inicializar_bd()

# Crear instancia de FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    version="0.1.0"
)

# Configurar CORS (opcional: ajustar dominios según necesidad)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas de la API
app.include_router(edge_router, prefix="/api")

@app.get("/", tags=["root"])
def read_root():
    return {"mensaje": "Nodo Edge activo", "entorno": settings.ENV}
