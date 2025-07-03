import os

# Configuración de PostgreSQL
PG_CONFIG = {
    "host": os.getenv("PG_HOST", "localhost"),
    "port": int(os.getenv("PG_PORT", 5432)),
    "database": os.getenv("PG_DB", "urbia_db"),
    "user": os.getenv("PG_USER", "urbia_user"),
    "password": os.getenv("PG_PASSWORD", "urbia_pass"),
}

# (opcional) SQLite
SQLITE_PATH = os.getenv("SQLITE_PATH", "data/edge_data.db")
