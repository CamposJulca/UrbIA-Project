# app/utils/sync_sqlite.py

import os
import shutil
from app.utils.logger import get_logger

logger = get_logger("sync_sqlite")

def sync_sqlite_from_local(
    source_path="/home/cristhiamdaniel/Desarrollo/urbia_fase0/services/nodo_edge/data/edge_data.db",
    target_path="data/edge_data.db"
):
    try:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copy2(source_path, target_path)
        logger.info(f"✅ Copia exitosa de {source_path} a {target_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Error al copiar el archivo SQLite: {e}")
        return False
