# 📊 Simulación Python + Dashboard Streamlit · UrbIA Fase 0

Este módulo permite **consultar, visualizar y exportar en tiempo real** los datos de sensores registrados en ThingsBoard. Incluye un **dashboard interactivo** en Streamlit y un script de lectura periódica que guarda los datos como CSV.

---

## 📁 Estructura del Proyecto

```

simulacion\_python/
├── config/
│   └── config.py              # Carga las variables del .env
├── core/
│   ├── api.py                 # Funciones para autenticación y consumo de API
│   └── lector.py              # Lector periódico y exportador de CSV
├── dashboard.py               # Dashboard Streamlit en tiempo real
├── main.py                    # Lanzador del dashboard
├── logs/
│   └── telemetria\_historica.csv  # Exportación automática del lector
├── .env                       # Variables sensibles

````

---

## 📦 Requisitos

- Python ≥ 3.9
- `streamlit`, `requests`, `pandas`, `python-dotenv`, `altair`

Instalación recomendada:

```bash
pip install -r requirements.txt
````

> ⚠️ Si no existe un `requirements.txt`, puedes instalar manualmente:

```bash
pip install streamlit requests pandas python-dotenv altair
```

---

## 🔐 Configuración

### 1. Crear archivo `.env`

En la raíz del módulo (`simulacion_python/`):

```env
THINGSBOARD_HOST=http://localhost:8080
DEVICE_TOKEN=<<TOKEN_DEL_DISPOSITIVO>>
TENANT_USER=admin@urbia.local
TENANT_PASSWORD=sysadmin
```

Este archivo se carga automáticamente gracias a `python-dotenv`.

---

## 🚀 Ejecutar el Dashboard

```bash
python main.py
```

Esto abrirá la app en `http://localhost:8504` (o un puerto dinámico).

### Funcionalidades del dashboard:

* Selección de dispositivo
* Filtro por variable y rango de tiempo
* KPIs en tiempo real (promedios, mínimos y máximos)
* Visualización con **Altair**
* Exportación a CSV

---

## 🧪 Ejecutar el lector automático

Este script lee periódicamente la telemetría y guarda un CSV con las últimas lecturas.

```bash
python core/lector.py
```

Parámetros por defecto:

* **Intervalo de consulta:** cada 5 minutos
* **Variables:** temperatura, humedad, co2, presión, luz, ruido
* **Archivo de salida:** `logs/telemetria_historica.csv`

---

## 🧩 Funciones clave

* `autenticar_tenant()` – Login en ThingsBoard
* `obtener_dispositivos()` – Lista de dispositivos activos
* `obtener_telemetria_historica()` – Lectura de datos históricos por rango

---

## 📊 Ejemplo de DataFrame generado

| timestamp           | sensor      | valor  |
| ------------------- | ----------- | ------ |
| 2025-06-29 10:50:01 | temperatura | 34.33  |
| 2025-06-29 10:50:01 | humedad     | 65.97  |
| 2025-06-29 10:50:01 | co2         | 477.0  |
| 2025-06-29 10:50:01 | presion     | 995.53 |
| 2025-06-29 10:50:01 | luz         | 675.29 |
| 2025-06-29 10:50:01 | ruido       | 50.27  |

---

## 📁 Exportación

Desde el dashboard puedes descargar los datos con un botón:

```
📥 Descargar CSV
```

El lector automático también los guarda en:

```
logs/telemetria_historica.csv
```

---

