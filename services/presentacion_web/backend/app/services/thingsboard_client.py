# backend/app/services/thingsboard_client.py

import requests
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()  # Cargar variables desde .env

class ThingsBoardClient:
    def __init__(self):
        self.base_url = os.getenv("THINGSBOARD_URL", "http://localhost:8080")
        self.username = os.getenv("THINGSBOARD_USER", "tenant@thingsboard.org")
        self.password = os.getenv("THINGSBOARD_PASSWORD", "tenant")
        self.token = self.autenticar()

    def autenticar(self) -> str:
        """
        Autenticación básica con ThingsBoard para obtener un token JWT.
        """
        url = f"{self.base_url}/api/auth/login"
        payload = {
            "username": self.username,
            "password": self.password
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            token = response.json().get("token")
            if not token:
                raise Exception("No se recibió token desde ThingsBoard.")
            print(f"[DEBUG] ✅ Token recibido: {token[:20]}...")  # Mostrar solo parte del token
            return token
        except requests.RequestException as e:
            raise Exception(f"[ERROR] ❌ Error al autenticar con ThingsBoard: {str(e)}")

    def _headers(self) -> Dict[str, str]:
        """
        Encabezados comunes con el token JWT.
        """
        return {
            "X-Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def obtener_dispositivos(self, limit: int = 50) -> List[Dict]:
        """
        Obtiene una lista de dispositivos registrados por el tenant.
        Si el token es inválido o expirado, intenta reautenticarse una vez.
        """
        url = f"{self.base_url}/api/tenant/devices?pageSize={limit}&page=0"


        def intento_obtener():
            print(f"[DEBUG] 🔗 Llamando a: {url}")
            print(f"[DEBUG] 📨 Headers: {self._headers()}")
            response = requests.get(url, headers=self._headers())
            if response.status_code == 401 or response.status_code == 400:
                print(f"[WARN] ⚠️ Token inválido. Reintentando autenticación...")
                self.token = self.autenticar()
                response = requests.get(url, headers=self._headers())
            response.raise_for_status()
            return response

        try:
            response = intento_obtener()
            data = response.json().get("data", [])
            dispositivos = [
                {
                    "id": d.get("id", {}).get("id"),
                    "nombre": d.get("name"),
                    "tipo": d.get("type"),
                    "activo": d.get("active", True),
                    "label": d.get("label", "")
                }
                for d in data
            ]
            print(f"[DEBUG] 📦 Dispositivos obtenidos: {len(dispositivos)}")
            return dispositivos
        except requests.RequestException as e:
            raise Exception(f"[ERROR] ❌ Error al obtener dispositivos: {str(e)}")
