# lector.py

#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.api import autenticar_tenant, obtener_dispositivos, obtener_telemetria_historica

print("✅ Lector ejecutado correctamente.")

import pandas as pd
import time
import os

# Configuración de variables
INTERVALO_MINUTOS = 5           # Cuánto tiempo atrás consultar
ESPERA_SEGUNDOS = 300           # Cada cuántos segundos hacer la lectura
VARIABLES = ["co2", "temperatura", "humedad", "presion", "luz", "ruido"]
ARCHIVO_SALIDA = "logs/telemetria_historica.csv"

def main():
    os.makedirs("logs", exist_ok=True)

    token = autenticar_tenant()
    if not token:
        print("❌ No se pudo autenticar.")
        return

    dispositivos = obtener_dispositivos(token)
    if not dispositivos:
        print("⚠️ No hay dispositivos.")
        return

    dispositivo = dispositivos[0]
    device_id = dispositivo["id"]["id"]
    print(f"📍 Usando dispositivo: {dispositivo['name']} ({device_id})")

    while True:
        df = obtener_telemetria_historica(device_id, token, keys=VARIABLES, minutos=INTERVALO_MINUTOS)
        if not df.empty:
            df.to_csv(ARCHIVO_SALIDA, index=False)
            print(f"✅ {len(df)} registros guardados en {ARCHIVO_SALIDA}")
        else:
            print("⚠️ No se obtuvieron datos en esta lectura.")

        print(f"🕒 Esperando {ESPERA_SEGUNDOS} segundos...\n")
        time.sleep(ESPERA_SEGUNDOS)

if __name__ == "__main__":
    main()
