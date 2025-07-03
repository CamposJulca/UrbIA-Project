# tests/test_jobs.py

import os
import sys
from pyspark.sql import SparkSession

# Agrega la ruta raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath("."))

from app.services.db_sqlite import read_from_sqlite  # ✅ CORRECTO

def main():
    print("🧪 Iniciando prueba de carga desde SQLite con Spark...")

    # Ruta al driver JDBC
    sqlite_jar_path = "/home/cristhiamdaniel/libs/sqlite-jdbc-3.42.0.0.jar"

    # Verifica que exista el .jar
    if not os.path.exists(sqlite_jar_path):
        raise FileNotFoundError(f"❌ No se encontró el driver JDBC en: {sqlite_jar_path}")

    # Iniciar SparkSession con el .jar
    spark = SparkSession.builder \
        .appName("Test ETL SQLite") \
        .config("spark.jars", sqlite_jar_path) \
        .getOrCreate()

    # Ejecutar carga desde SQLite
    df = read_from_sqlite(spark)

    if df is None or df.rdd.isEmpty():
        print("⚠️ No se cargaron datos desde SQLite.")
    else:
        print(f"✅ Carga exitosa: {df.count()} registros.")
        df.show(truncate=False)

    spark.stop()

if __name__ == "__main__":
    main()
