# Lógica de procesamiento por lotes

import sqlite3
from datetime import datetime
from collections import defaultdict

DB_PATH = "data/edge_data.db"

def procesar_lecturas_por_lote():
    """
    Procesa las lecturas registradas y calcula el promedio por dispositivo y variable.
    Guarda los resultados en la tabla resumen_edge.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Asegurar que exista la tabla resumen_edge
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resumen_edge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                variable TEXT NOT NULL,
                promedio REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)

        # Leer lecturas actuales
        cursor.execute("SELECT device_id, variable, valor FROM lecturas_edge")
        rows = cursor.fetchall()

        if not rows:
            print("⚠️ No hay lecturas registradas para procesar.")
            return {"mensaje": "No hay datos para procesar"}

        # Agrupar y calcular promedios
        datos_agrupados = defaultdict(list)
        for device_id, variable, valor in rows:
            datos_agrupados[(device_id, variable)].append(valor)

        timestamp_actual = datetime.utcnow().isoformat()

        # Insertar resultados
        for (device_id, variable), valores in datos_agrupados.items():
            promedio = sum(valores) / len(valores)
            cursor.execute("""
                INSERT INTO resumen_edge (device_id, variable, promedio, timestamp)
                VALUES (?, ?, ?, ?)
            """, (device_id, variable, promedio, timestamp_actual))

        conn.commit()
        print("✅ Procesamiento por lote completado.")
        return {"mensaje": "Lote procesado exitosamente", "registros": len(datos_agrupados)}

    except Exception as e:
        print(f"❌ Error durante el procesamiento por lote: {e}")
        return {"error": str(e)}

    finally:
        conn.close()
