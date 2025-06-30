#!/bin/bash
echo "🚀 Ejecutando UrbIA CLI para ThingsBoard..."

# Validar existencia del archivo .env
if [ ! -f .env ]; then
  echo "❌ Archivo .env no encontrado en $(pwd)"
  exit 1
fi

# Compilar y ejecutar con Maven
mvn clean compile exec:java -Dexec.mainClass="urbia.cli.Main"
