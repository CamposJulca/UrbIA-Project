#!/bin/bash

echo "🚀 Iniciando módulo presentacion_web (UrbIA)..."

echo "🧠 Iniciando backend (FastAPI)..."
cd backend || exit
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

echo "🌐 Iniciando frontend (Vite/React)..."
cd frontend || exit
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ Backend y frontend ejecutándose en segundo plano."
echo "🌍 Accede a: http://localhost:8000/docs (API) y http://localhost:5173 (Frontend)"

# Esperar a que ambos procesos terminen
wait $BACKEND_PID $FRONTEND_PID
