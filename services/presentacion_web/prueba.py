import requests

URL = "http://localhost:8080"
USER = "tenant@thingsboard.org"
PASSWORD = "tenant"

# Paso 1: Autenticación
login_url = f"{URL}/api/auth/login"
login_resp = requests.post(login_url, json={"username": USER, "password": PASSWORD})
print("[AUTH STATUS]", login_resp.status_code)
print("[AUTH BODY]", login_resp.text)
token = login_resp.json().get("token")
headers = {"X-Authorization": f"Bearer {token}"}

# Paso 2: Consulta moderna de dispositivos
device_url = f"{URL}/api/tenant/devices"
params = {
    "pageSize": 50,
    "page": 0,
    "sortProperty": "name",
    "sortOrder": "asc"
}
device_resp = requests.get(device_url, headers=headers, params=params)
print("[DEVICE STATUS]", device_resp.status_code)
print("[DEVICE BODY]", device_resp.text)
