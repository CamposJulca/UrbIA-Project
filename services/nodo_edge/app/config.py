# Parámetros globales y helpers de configuración

import os
from dotenv import load_dotenv

# Cargar variables desde .env si existe
load_dotenv()

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuración general
class Settings:
    PROJECT_NAME: str = "Nodo Edge - UrbIA"
    ENV: str = os.getenv("ENV", "development")
    DB_PATH: str = os.getenv("DB_PATH", os.path.join(BASE_DIR, "data", "edge_data.db"))
    LOG_PATH: str = os.getenv("LOG_PATH", os.path.join(BASE_DIR, "logs", "edge_node.log"))
    DEBUG: bool = ENV != "production"

settings = Settings()
