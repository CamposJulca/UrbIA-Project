# Configuración y conexión SQLite

import sqlite3
from app.config import settings

def get_connection():
    """Devuelve una conexión SQLite a la base de datos local."""
    return sqlite3.connect(settings.DB_PATH)

def inicializar_bd():
    """Crea las tablas necesarias si no existen."""
    conn = get_connection()
    cursor = conn.cursor()

    # Crear tabla de lecturas crudas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lecturas_edge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            variable TEXT NOT NULL,
            valor REAL NOT NULL
        )
    """)

    # Crear tabla de resumen por lote (si no ha sido creada por batch.py)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumen_edge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            variable TEXT NOT NULL,
            promedio REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente.")
