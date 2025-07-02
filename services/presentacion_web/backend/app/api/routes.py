# backend/app/api/routes.py

from fastapi import APIRouter, HTTPException
from app.services.thingsboard_client import ThingsBoardClient
# from app.api.endpoints import devices, telemetry  # asegúrate de importar todos

router = APIRouter()

tb_client = ThingsBoardClient()

@router.get("/ping", tags=["Prueba"])
def ping():
    """Ruta de prueba básica para verificar que el API está activa"""
    return {"message": "UrbIA backend is alive 🚀"}

@router.get("/devices", tags=["ThingsBoard"])
def listar_dispositivos():
    """
    Consulta todos los dispositivos disponibles en ThingsBoard.
    Retorna una lista con ID, nombre, tipo y estado de cada dispositivo.
    """
    try:
        dispositivos = tb_client.obtener_dispositivos()
        return {"dispositivos": dispositivos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener dispositivos: {str(e)}")
