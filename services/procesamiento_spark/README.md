# 🔥 Procesamiento Spark — UrbIA · Fase 0

Este módulo ejecuta trabajos de Spark sobre los datos telemétricos recopilados por el Nodo Edge y los almacena en PostgreSQL para análisis posterior.

## 📂 Estructura

- `app/core/`: lógica de procesamiento (Spark jobs)
- `app/services/`: conectores a bases de datos (SQLite/PostgreSQL)
- `app/schemas/`: validación de datos
- `app/utils/`: utilidades generales (logs, temporizadores)
- `scripts/`: ejecución como batch o servicio
- `tests/`: pruebas unitarias
- `Dockerfile`: contenedor opcional

## ⚙️ Requisitos

- Python 3.10+
- PySpark
- PostgreSQL y/o SQLite

## 🚀 Ejecución

```bash
bash scripts/run_job.sh
```

## 📦 Variables de entorno (.env)

```
SQLITE_PATH=data/edge_data.db
POSTGRES_URI=postgresql://user:pass@localhost:5432/urbia_db
```

