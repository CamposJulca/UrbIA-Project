#!/bin/bash

echo "🚧 Creando estructura de la nueva aplicación web UrbIA..."

# Backend (FastAPI)
mkdir -p backend/app/api
mkdir -p backend/app/core
mkdir -p backend/app/models
mkdir -p backend/app/services
mkdir -p backend/app/utils
mkdir -p backend/tests
mkdir -p backend/logs

touch backend/app/__init__.py
touch backend/app/api/__init__.py
touch backend/app/core/__init__.py
touch backend/app/models/__init__.py
touch backend/app/services/__init__.py
touch backend/app/utils/__init__.py
touch backend/tests/__init__.py

# Archivos principales del backend
touch backend/app/main.py
touch backend/app/core/config.py
touch backend/app/services/thingsboard_client.py
touch backend/app/api/routes.py
touch backend/requirements.txt
touch backend/.env.example
touch backend/logs/.gitkeep

# Frontend base (para React o similar)
mkdir -p frontend/public
mkdir -p frontend/src/components
mkdir -p frontend/src/pages
mkdir -p frontend/src/services
mkdir -p frontend/src/assets

touch frontend/src/index.js
touch frontend/src/App.js
touch frontend/src/services/api.js
touch frontend/package.json
touch frontend/.env.example

# Documentación
touch README.md

echo "✅ Estructura creada correctamente."
