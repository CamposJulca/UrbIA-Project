# Pruebas unitarias para los endpoints de FastAPI

import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_ping():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/ping")
    assert response.status_code == 200
    assert "Nodo Edge activo" in response.json()["mensaje"]

@pytest.mark.asyncio
async def test_telemetria_y_lecturas():
    # Enviar lote de lecturas
    lecturas = {
        "lecturas": [
            {
                "device_id": "sensor-001",
                "timestamp": "2025-07-02T10:00:00",
                "variable": "temperatura",
                "valor": 23.5
            },
            {
                "device_id": "sensor-001",
                "timestamp": "2025-07-02T10:00:10",
                "variable": "humedad",
                "valor": 60.2
            }
        ]
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        post_response = await ac.post("/api/telemetria", json=lecturas)
        assert post_response.status_code == 200
        assert "lecturas" in post_response.json()["mensaje"]

        get_response = await ac.get("/api/lecturas?limit=2")
        assert get_response.status_code == 200
        data = get_response.json()
        assert len(data) >= 2
        assert all("device_id" in lectura for lectura in data)

@pytest.mark.asyncio
async def test_procesar_lote_y_resumen():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Procesar lote
        proc_response = await ac.post("/api/procesar-lote")
        assert proc_response.status_code == 200
        assert "Lote procesado exitosamente" in proc_response.json()["mensaje"]

        # Consultar resumen
        resumen_response = await ac.get("/api/resumen?limit=1")
        assert resumen_response.status_code == 200
        data = resumen_response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "promedio" in data[0]
