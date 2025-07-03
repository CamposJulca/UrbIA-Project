# 🧠 Nodo Edge - UrbIA Fase 0

Este módulo implementa el nodo Edge de la arquitectura UrbIA. Es responsable de recibir telemetría de sensores, almacenarla temporalmente en SQLite y procesarla periódicamente por lotes. Sirve como puente entre la simulación IoT y futuras etapas de análisis o persistencia centralizada.

---

## 📁 Estructura del proyecto

```

nodo\_edge/
├── app/                     # Lógica de la API FastAPI
│   ├── batch.py             # Procesamiento por lotes
│   ├── config.py            # Configuración general
│   ├── database.py          # Conexión SQLite
│   ├── main.py              # Servidor FastAPI
│   ├── models.py            # ORM con SQLAlchemy
│   └── routes.py            # Endpoints de la API
├── data/
│   └── edge\_data.db         # Base SQLite (opcional, si persiste)
├── logs/
│   └── edge\_node.log        # Log de operaciones
├── simulador/
│   └── enviar\_lecturas.py   # Simulador de lecturas IoT
├── tests/
│   └── test\_api.py          # Pruebas unitarias
├── estructura\_nodo\_edge.sh  # Script inicial (opcional)
├── requirements.txt         # Dependencias del proyecto
├── README.md                # Este documento

````

---

## 🚀 Cómo ejecutar esta capa

### 1. Clonar el repositorio (o navegar al directorio `nodo_edge`)
```bash
cd ~/Desarrollo/urbia_fase0/services/nodo_edge
````

### 2. Activar entorno virtual

```bash
source ../../.venv/bin/activate
```

### 3. Instalar dependencias (solo la primera vez)

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el servidor FastAPI

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8010
```

* El nodo queda escuchando en: `http://localhost:8010`
* Puedes verificar que está activo con:

```bash
curl http://localhost:8010/api/ping
```

---

## 📡 Ejecutar el simulador IoT

Abre otra terminal con el entorno virtual activado y ejecuta:

```bash
cd simulador
python enviar_lecturas.py
```

Este script enviará lecturas simuladas cada 10 segundos y procesará automáticamente un lote cada 60 segundos.

---

## 🔍 Endpoints útiles

* `GET /api/ping` – Verifica si el nodo está activo
* `POST /api/telemetria` – Envía lecturas simuladas
* `POST /api/procesar-lote` – Procesa manualmente un lote
* `GET /api/lecturas` – Consulta lecturas crudas
* `GET /api/resumen` – Consulta resultados resumidos por variable

---

## 📌 Notas

* El nodo Edge usa SQLite como almacenamiento temporal local.
* Se planea agregar exportación a PostgreSQL y métricas avanzadas.
* Forma parte de la **Fase 0** del proyecto UrbIA.

---
