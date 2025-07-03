#!/bin/bash

echo "🛠️ Generando estructura de carpetas y archivos para procesamiento Spark..."

# Crear subdirectorios dentro de procesamiento_spark/
mkdir -p app/core
mkdir -p app/config
mkdir -p app/services
mkdir -p app/schemas
mkdir -p app/utils
mkdir -p scripts
mkdir -p tests

# Crear archivos base con contenido útil
echo "# Lógica principal del procesamiento Spark" > app/core/jobs.py

cat <<EOF > app/config/settings.py
# Configuración del entorno (SQLite y PostgreSQL)

import os

SQLITE_PATH = os.getenv("SQLITE_PATH", "data/edge_data.db")
POSTGRES_URI = os.getenv("POSTGRES_URI", "postgresql://user:pass@localhost:5432/urbia_db")
EOF

echo "# Conector para leer desde SQLite" > app/services/db_sqlite.py
echo "# Conector para escribir en PostgreSQL" > app/services/db_postgres.py
echo "# Modelo de esquema para métricas procesadas" > app/schemas/metrics_schema.py
echo "# Logger básico para auditoría interna" > app/utils/logger.py
echo "# Utilidad para medir tiempos de ejecución" > app/utils/timer.py

cat <<EOF > scripts/run_job.sh
#!/bin/bash
# Script para ejecutar el job principal de Spark
echo '🚀 Ejecutando procesamiento Spark...'
python3 -m app.core.jobs
EOF

chmod +x scripts/run_job.sh

echo "# Prueba inicial para los Spark Jobs" > tests/test_jobs.py
echo "pyspark\npsycopg2-binary\ndotenv" > requirements.txt
echo "SQLITE_PATH=data/edge_data.db\nPOSTGRES_URI=postgresql://user:pass@localhost:5432/urbia_db" > .env

cat <<EOF > Dockerfile
# Dockerfile para microservicio de procesamiento Spark

FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash", "scripts/run_job.sh"]
EOF

cat <<EOF > README.md
# 🔥 Procesamiento Spark — UrbIA · Fase 0

Este módulo ejecuta trabajos de Spark sobre los datos telemétricos recopilados por el Nodo Edge y los almacena en PostgreSQL para análisis posterior.

## 📂 Estructura

- \`app/core/\`: lógica de procesamiento (Spark jobs)
- \`app/services/\`: conectores a bases de datos (SQLite/PostgreSQL)
- \`app/schemas/\`: validación de datos
- \`app/utils/\`: utilidades generales (logs, temporizadores)
- \`scripts/\`: ejecución como batch o servicio
- \`tests/\`: pruebas unitarias
- \`Dockerfile\`: contenedor opcional

## ⚙️ Requisitos

- Python 3.10+
- PySpark
- PostgreSQL y/o SQLite

## 🚀 Ejecución

\`\`\`bash
bash scripts/run_job.sh
\`\`\`

## 📦 Variables de entorno (.env)

\`\`\`
SQLITE_PATH=data/edge_data.db
POSTGRES_URI=postgresql://user:pass@localhost:5432/urbia_db
\`\`\`

EOF

echo "✅ Estructura creada dentro de $(pwd)"
