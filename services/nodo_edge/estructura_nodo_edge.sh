#!/bin/bash

echo "🔧 Creando estructura base para nodo_edge..."

# Crear carpetas
mkdir -p app data tests logs

# Crear archivos vacíos con comentarios iniciales
touch app/main.py
echo "# Punto de entrada FastAPI" > app/main.py

touch app/database.py
echo "# Configuración y conexión SQLite" > app/database.py

touch app/models.py
echo "# Definición de modelos y esquemas de base de datos" > app/models.py

touch app/routes.py
echo "# Endpoints principales del nodo_edge" > app/routes.py

touch app/batch.py
echo "# Lógica de procesamiento por lotes" > app/batch.py

touch app/config.py
echo "# Parámetros globales y helpers de configuración" > app/config.py

touch data/edge_data.db  # archivo vacío, se llenará en tiempo de ejecución

touch tests/test_api.py
echo "# Pruebas unitarias para los endpoints de FastAPI" > tests/test_api.py

touch logs/edge_node.log  # archivo de log vacío

# Crear archivos raíz
touch requirements.txt
echo "# Requisitos del proyecto nodo_edge (FastAPI, SQLite, etc.)" > requirements.txt

touch .env
echo "# Variables de entorno para configuración local" > .env

touch README.md
echo "# Nodo Edge - UrbIA\n\nMicroservicio local para procesamiento por lotes con FastAPI y SQLite." > README.md

echo "✅ Estructura creada correctamente en $(pwd)"
