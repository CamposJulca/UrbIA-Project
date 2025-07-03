import requests
import random
import time
from datetime import datetime, timezone
import logging

# Configurar logging a archivo
logging.basicConfig(
    filename='simulador.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# Variables disponibles para simular
variables = ["temperatura", "humedad", "presion", "luminosidad"]
# Lista de sensores simulados
sensores = [f"sensor-00{i}" for i in range(1, 6)]

URL_TELEMETRIA = "http://localhost:8010/api/telemetria"
URL_PROCESAR = "http://localhost:8010/api/procesar-lote"

print("🌐 Iniciando simulador de lecturas IoT con múltiples sensores y procesamiento periódico...")

ciclo = 0
while True:
    lecturas = []
    for _ in range(2):  # Generar 2 lecturas por ciclo
        sensor = random.choice(sensores)
        variable = random.choice(variables)
        valor = round(random.uniform(20.0, 1000.0), 2)
        timestamp = datetime.now(timezone.utc).isoformat()
        lecturas.append({
            "device_id": sensor,
            "timestamp": timestamp,
            "variable": variable,
            "valor": valor
        })

    payload = {"lecturas": lecturas}

    try:
        response = requests.post(URL_TELEMETRIA, json=payload)
        msg = f"[{timestamp}] Enviado: {payload}\n📨 Respuesta: {response.status_code} {response.text}"
        print(msg)
        logging.info(f"Enviado: {payload} | Respuesta: {response.status_code} {response.text}")
    except Exception as e:
        logging.error(f"Error al enviar lecturas: {e}")

    ciclo += 1
    if ciclo % 6 == 0:  # Cada 6 ciclos (~60s)
        try:
            r_proc = requests.post(URL_PROCESAR)
            print(f"[{datetime.now()}] ⚙️ Procesado lote: {r_proc.status_code} {r_proc.text}")
            logging.info(f"Procesado lote: {r_proc.status_code} {r_proc.text}")
        except Exception as e:
            logging.error(f"Error al procesar lote: {e}")

    time.sleep(10)
