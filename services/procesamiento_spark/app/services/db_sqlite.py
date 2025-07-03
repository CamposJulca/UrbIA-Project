import os
from pyspark.sql import SparkSession
from app.utils.logger import get_logger

logger = get_logger("db_sqlite")

def read_from_sqlite(spark: SparkSession):
    """
    Carga una tabla de SQLite como DataFrame de Spark utilizando JDBC.

    Parámetros:
    - spark: sesión activa de Spark

    Variables de entorno requeridas:
    - SQLITE_PATH: ruta completa del archivo .db (por defecto: data/edge_data.db)
    - SQLITE_TABLE: nombre de la tabla a cargar (por defecto: resumen_edge)

    Retorna:
    - DataFrame de Spark o None si ocurre un error.
    """
    db_path = os.getenv("SQLITE_PATH", "data/edge_data.db")
    table = os.getenv("SQLITE_TABLE", "resumen_edge")
    url = f"jdbc:sqlite:{db_path}"

    logger.info(f"🔌 Conectando a SQLite: {db_path}, tabla: {table}")

    try:
        df = spark.read \
            .format("jdbc") \
            .option("url", url) \
            .option("dbtable", table) \
            .option("driver", "org.sqlite.JDBC") \
            .load()

        logger.info(f"📥 Datos cargados correctamente desde SQLite ({table})")
        return df

    except Exception as e:
        logger.error(f"❌ Error al leer desde SQLite con Spark: {e}")
        return None
