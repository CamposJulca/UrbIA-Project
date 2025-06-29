#!/bin/bash

echo "🚀 Iniciando entorno UrbIA Fase 0..."
cd "$(dirname "$0")" || exit 1

# Definir rutas
CPP_DIR="./simulador_cpp"
PYTHON_DIR="./simulacion_python"
JAVA_DIR="./simulacion_gateway"

# Ejecutar simulador C++ (en segundo plano)
echo "🟦 Ejecutando simulador C++..."
(cd "$CPP_DIR" && ./sensor_simulator >> logs/simulador.log 2>&1 &)  # Redirige logs

# Ejecutar dashboard Streamlit (en segundo plano)
echo "🐍 Ejecutando dashboard Streamlit..."
(cd "$PYTHON_DIR" && streamlit run dashboard.py --server.port 8516 >> logs/streamlit.log 2>&1 &)  # Redirige logs

# Ejecutar cliente Java CLI (en primer plano)
echo "☕ Ejecutando cliente Java CLI..."
(cd "$JAVA_DIR" && mvn clean package exec:java)

echo "✅ Todos los servicios han sido iniciados correctamente."
