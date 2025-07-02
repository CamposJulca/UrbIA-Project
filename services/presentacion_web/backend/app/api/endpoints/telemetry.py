from fastapi import APIRouter
from app.services.thingsboard import get_device_telemetry

router = APIRouter()

@router.get("/telemetry/{device_id}", tags=["ThingsBoard"])
async def obtener_telemetria(device_id: str):
    return get_device_telemetry(device_id)
