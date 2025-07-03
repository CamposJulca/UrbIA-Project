# app/core/jobs.py

import os
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, min, max, to_timestamp

from app.utils.logger import get_logger
from app.utils.timer import timed
from app.services.db_postgres import insert_metrics
from app.schemas.metrics_schema import SensorMetric

logger = get_logger(__name__)

def read_from_sqlite(spark: SparkSession):
    path = os.getenv('SQLITE_DB_PATH')
    table = os.getenv("SQLITE_TABLE", "resumen_edge")

    print(f"🔍 Intentando leer SQLite desde: {path}")
    print(f"📋 Tabla objetivo: {table}")

    if not os.path.exists(path):
        print(f"❌ El archivo SQLite no existe en {path}")
        return None

    url = f"jdbc:sqlite:{path}"

    try:
        df = spark.read \
            .format("jdbc") \
            .option("url", url) \
            .option("dbtable", table) \
            .option("driver", "org.sqlite.JDBC") \
            .load()

        # Detectar y renombrar columnas si vienen con nombres alternos
        column_map = {
            "device_id": "sensor_id",
            "variable": "tipo",
            "promedio": "valor"
        }

        for old_col, new_col in column_map.items():
            if old_col in df.columns:
                df = df.withColumnRenamed(old_col, new_col)

        expected_cols = {"sensor_id", "tipo", "valor", "timestamp"}
        if not expected_cols.issubset(set(df.columns)):
            print(f"❌ Las columnas requeridas no están completas. Se requieren: {expected_cols}")
            logger.error(f"❌ Columnas faltantes en la tabla {table}")
            return None

        count = df.count()
        print(f"✅ Datos cargados desde SQLite con {count} registros.")
        df.show(5, truncate=False)
        logger.info(f"📥 Datos cargados correctamente desde SQLite ({table})")
        return df

    except Exception as e:
        logger.error(f"❌ Error al leer desde SQLite con Spark: {e}")
        print(f"❌ Error al leer desde SQLite con Spark: {e}")
        return None


@timed
def run_etl_job():
    print("🚀 Entrando a run_etl_job...")
    logger.info("🚀 Iniciando Spark Job de procesamiento de métricas...")

    spark = SparkSession.builder \
        .appName("UrbIA - Spark Processing") \
        .getOrCreate()
    print("✅ SparkSession creada.")

    df = read_from_sqlite(spark)
    if df is None or df.rdd.isEmpty():
        print("⚠️ No se encontraron datos válidos.")
        logger.warning("⚠️ No se encontraron datos en la tabla seleccionada.")
        spark.stop()
        return

    print(f"📦 Total registros leídos: {df.count()}")
    logger.info(f"📦 Registros leídos desde SQLite: {df.count()}")

    try:
        df = df.withColumn("ts", to_timestamp(col("timestamp")))
        df = df.select("sensor_id", "tipo", "valor", "ts")
        print("🧪 Preprocesamiento completado.")
        df.show(5)
    except Exception as e:
        print(f"❌ Error en preprocesamiento: {e}")
        logger.error(f"❌ Error en preprocesamiento: {e}")
        spark.stop()
        return

    try:
        agg_df = df.groupBy("sensor_id", "tipo") \
            .agg(
                avg("valor").alias("promedio"),
                min("valor").alias("minimo"),
                max("valor").alias("maximo"),
                max("ts").alias("timestamp")
            )

        # 🔧 Corrección de tipo 'luminosidad' a 'luz' para validación
        from pyspark.sql import functions as F
        agg_df = agg_df.withColumn(
            "tipo",
            F.when(F.col("tipo") == "luminosidad", "luz").otherwise(F.col("tipo"))
        )

        print("📊 Agregación completada.")
        agg_df.show(5)
        logger.info(f"📊 Datos agregados: {agg_df.count()} métricas")

    except Exception as e:
        print(f"❌ Error durante la agregación: {e}")
        logger.error(f"❌ Error en la agregación de datos: {e}")
        spark.stop()
        return

    metricas = []
    errores = 0

    for row in agg_df.collect():
        try:
            metrica = SensorMetric(
                sensor_id=row["sensor_id"],
                tipo=row["tipo"],
                promedio=row["promedio"],
                minimo=row["minimo"],
                maximo=row["maximo"],
                timestamp=row["timestamp"]
            )
            metricas.append(metrica.dict())
        except Exception as e:
            errores += 1
            print(f"❌ Error validando fila: {row} -> {e}")
            logger.warning(f"❌ Error de validación para {row['sensor_id']}: {e}")

    print(f"✅ {len(metricas)} métricas válidas, ❌ {errores} con errores de validación.")
    logger.info(f"✅ {len(metricas)} métricas válidas, ❌ {errores} con errores de validación.")

    if metricas:
        try:
            print("📤 Insertando métricas en PostgreSQL...")
            insert_metrics(metricas)
        except Exception as e:
            print(f"❌ Error insertando en PostgreSQL: {e}")
            logger.error(f"❌ Fallo al insertar métricas: {e}")
    else:
        print("⚠️ No hay métricas válidas para insertar.")
        logger.warning("⚠️ Métricas vacías. No se insertó nada.")

    try:
        output_path = "data/metricas_agg.csv"
        agg_df.toPandas().to_csv(output_path, index=False)
        print(f"📝 CSV guardado: {output_path}")
        logger.info(f"📝 CSV generado correctamente: {output_path}")
    except Exception as e:
        print(f"❌ Error guardando CSV: {e}")
        logger.warning(f"❌ No se pudo guardar CSV: {e}")

    spark.stop()
    print("✅ Spark Job finalizado correctamente.")
    logger.info("✅ Spark Job finalizado correctamente.")


if __name__ == "__main__":
    print("🔧 Iniciando desde main...")
    run_etl_job()
