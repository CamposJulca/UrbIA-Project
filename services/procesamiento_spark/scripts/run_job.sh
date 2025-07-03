#!/bin/bash

echo "🔧 Iniciando ejecución completa del Job UrbIA..."

# 1. Activar entorno virtual
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Entorno virtual activado."
else
    echo "⚠️ Entorno virtual no encontrado. Continúa sin activación."
fi

# 2. Cargar variables de entorno
if [ -f ".env" ]; then
    echo "📦 Cargando variables de entorno desde .env"
    export $(grep -v '^#' .env | xargs)
else
    echo "⚠️ Archivo .env no encontrado. Se usarán valores por defecto si aplica."
fi

# 3. Definir fecha y ruta de ejecución
FECHA_EJECUCION=$(date +"%Y-%m-%d_%H-%M-%S")
CARPETA_EJECUCION="data/ejecuciones/$FECHA_EJECUCION"
mkdir -p "$CARPETA_EJECUCION"

# 4. Configurar PYTHONPATH
export PYTHONPATH=$(pwd)
echo "🔍 PYTHONPATH configurado en: $PYTHONPATH"

# 5. Validar existencia del driver JDBC
if [ -z "$SQLITE_JAR_PATH" ] || [ ! -f "$SQLITE_JAR_PATH" ]; then
    echo "❌ Error: SQLITE_JAR_PATH no definido o el archivo .jar no existe en $SQLITE_JAR_PATH"
    exit 1
else
    echo "🧩 Usando driver JDBC: $SQLITE_JAR_PATH"
fi

# 6. Ejecutar Spark Job
echo "🚀 Ejecutando procesamiento Spark..."
spark-submit --jars "$SQLITE_JAR_PATH" app/core/jobs.py
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo "❌ Error en Spark Job. Código de salida: $EXIT_CODE"
    exit $EXIT_CODE
fi
echo "✅ Spark Job finalizado con éxito."

# 7. Mover CSV generado a carpeta de ejecución
CSV_ORIGINAL="data/metricas_agg.csv"
if [ ! -f "$CSV_ORIGINAL" ]; then
    echo "❌ No se encontró el archivo $CSV_ORIGINAL"
    exit 1
fi

CSV_FINAL="$CARPETA_EJECUCION/metricas_agg.csv"
mv "$CSV_ORIGINAL" "$CSV_FINAL"
echo "📝 CSV movido a: $CSV_FINAL"

# 8. Ejecutar visualización
echo "📊 Generando gráficas con matplotlib..."
python scripts/visualizar_metricas.py "$CSV_FINAL" "$CARPETA_EJECUCION"

# 9. Verificación final
GRAFICAS_GENERADAS=$(ls "$CARPETA_EJECUCION"/grafico_sensor_*.png 2>/dev/null | wc -l)
echo "📈 $GRAFICAS_GENERADAS gráficas guardadas en: $CARPETA_EJECUCION"

echo "🎉 Proceso completo finalizado correctamente en $FECHA_EJECUCION"
