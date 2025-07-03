# Conector para escribir en PostgreSQL

import psycopg2
from psycopg2.extras import execute_values
from app.utils.logger import get_logger
from app.config.settings import PG_CONFIG

logger = get_logger("db_postgres")

def insert_metrics(metrics: list[dict], table_name: str = "metrics_summary") -> None:
    if not metrics:
        logger.warning("⚠️ No hay métricas para insertar en PostgreSQL.")
        return

    try:
        conn = psycopg2.connect(**PG_CONFIG)
        cur = conn.cursor()

        columns = metrics[0].keys()
        values = [[m[col] for col in columns] for m in metrics]

        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"
        execute_values(cur, query, values)

        conn.commit()
        cur.close()
        conn.close()

        logger.info(f"📤 Insertadas {len(metrics)} métricas en PostgreSQL.")
    except Exception as e:
        logger.error(f"❌ Error al insertar métricas en PostgreSQL: {e}")
