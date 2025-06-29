# 🧠 UrbIA: Urban Intelligence Architecture

**UrbIA** es una arquitectura modular, escalable y de código abierto para la inteligencia urbana distribuida. El proyecto nace como extensión aplicada de una tesis de maestría, integrando tecnologías modernas como **Edge Computing**, **SDN**, **IoT**, y **Ciencia de Datos**, con una implementación multilenguaje basada en microservicios (Python, C++, Java).

Este repositorio contiene la **Fase 0: Simulación Local**, punto de partida para validar la arquitectura conceptual mediante sensores simulados, nodos edge locales y monitoreo interno.

---

## 🎯 Objetivos

- Simular sensores urbanos heterogéneos (CO₂, temperatura, ruido, etc.)
- Enviar datos a una plataforma IoT (ThingsBoard) vía protocolos REST
- Procesar localmente eventos mediante un nodo Edge con FastAPI y SQLite
- Visualizar métricas vía Streamlit y Grafana
- Integrar procesamiento analítico con Spark
- Establecer una arquitectura lista para escalar en fases futuras

---

## 🧱 Arquitectura General

> Diagrama completo disponible en [`docs/diagramas/`](docs/diagramas/)

La arquitectura está dividida en capas, respetando principios de separación de responsabilidades y orientada a microservicios:

1. **Capa de Presentación**:
   - Web (Streamlit)
   - CLI (Java Terminal)
2. **Simulación IoT**:
   - Simulador C++ con libcurl
   - Cliente Python consumidor REST
   - Gateway Java emulando dispositivos
3. **Procesamiento Edge**:
   - FastAPI + SQLite
4. **Plataforma IoT**:
   - ThingsBoard CE local
5. **Ciencia de Datos**:
   - Jobs Spark (simulados)
6. **Persistencia**:
   - PostgreSQL local
7. **Monitorización**:
   - Grafana configurado localmente
8. **Red SDN**:
   - Controlador Ryu + topología simulada

---

## 🧪 Estructura del Repositorio

```plaintext
urbia_fase0/
├── docs/                  # Documentación técnica y diagramas
├── shared/                # Código reutilizable y configuraciones comunes
├── logs/                  # Logs centralizados
├── services/              # Microservicios organizados por capa
│   ├── presentacion_web/      # Streamlit
│   ├── presentacion_cli/      # Terminal Java
│   ├── simulacion_gateway/    # Gateway Java REST
│   ├── simulacion_python/     # Cliente REST Python
│   ├── simulador_cpp/         # Sensores simulados en C++
│   ├── nodo_edge/             # FastAPI + SQLite
│   ├── plataforma_thingsboard/
│   ├── procesamiento_spark/
│   ├── persistencia_pg/
│   ├── monitoreo_grafana/
│   └── red_sdn/
├── docker-compose.yml     # Contenerización opcional
├── .env                   # Variables de entorno comunes
├── .gitignore
├── README.md
└── requirements.txt
````

---

## 🔀 Ramas del Proyecto

| Rama               | Descripción                             |
| ------------------ | --------------------------------------- |
| `fase0-simulacion` | Simulación local con sensores virtuales |
| `fase1-desarrollo` | Desarrollo en servidor de pruebas       |
| `fase2-testing`    | QA e integración en entorno de testing  |
| `fase3-despliegue` | Despliegue final en producción          |

---

## 🚀 Requisitos para ejecutar Fase 0

* Python 3.10+
* Java 17+
* CMake + G++
* Docker (para ThingsBoard opcionalmente)
* PostgreSQL (local)
* Grafana (instalación local)
* Entorno virtual: `.venv` configurado con `requirements.txt`

---

## 📦 Instalación básica

```bash
git clone https://github.com/CamposJulca/UrbIA-Project.git
cd urbia_fase0
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🧑‍💻 Colaboraciones

Este proyecto busca ser **abierto, académico y replicable**. Si eres estudiante, docente o investigador interesado en contribuir, puedes crear tus propias ramas, reportar problemas o sugerir mejoras.

---

## 📄 Licencia

Proyecto liberado bajo licencia **MIT** para uso académico, educativo y de investigación.

---

## 📫 Contacto

**Cristhiam Daniel Campos Julca**
GitHub: [@CamposJulca](https://github.com/CamposJulca)

Correo: [ccamposj@unal.edu.co](mailto:ccamposj@unal.edu.co)

