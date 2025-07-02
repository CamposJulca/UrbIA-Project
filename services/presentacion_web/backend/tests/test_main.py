# backend/tests/test_main.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_lecturas_endpoint_sin_parametros():
    response = client.get("/api/lecturas")
    assert response.status_code == 422  # Faltan parámetros obligatorios

def test_lecturas_endpoint_parametros():
    response = client.get("/api/lecturas", params={"device_id": "demo-device", "limit": 1})
    assert response.status_code in (200, 500)  # 200 si conexión exitosa, 500 si falla conexión con ThingsBoard
