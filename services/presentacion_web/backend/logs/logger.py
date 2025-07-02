# backend/logs/logger.py

import logging
import os

# Crear directorio de logs si no existe
LOG_DIR = "backend/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Ruta del archivo de log
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("urbia-backend")
