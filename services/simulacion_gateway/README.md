# ☕ Simulación Gateway Java · UrbIA Fase 0

Este módulo implementa un **cliente Java CLI** que se conecta a la plataforma ThingsBoard para:

- 🔐 Autenticarse como tenant
- 📡 Listar los dispositivos conectados
- 📥 Obtener lecturas recientes de sensores
- 💾 Exportar lecturas a archivos CSV

Forma parte del ecosistema UrbIA de monitoreo urbano inteligente (Fase 0).

---

## 📁 Estructura del Proyecto

```

simulacion\_gateway/
├── config/                        # Configuración adicional
├── src/main/java/urbia/          # Código fuente
│   ├── Main.java                 # Interfaz principal CLI
│   ├── api/
│   │   ├── HttpUtils.java       # Cliente HTTP
│   │   ├── JsonUtils.java       # Utilidades JSON
│   │   └── ThingsBoardClient.java
│   └── models/
│       └── SensorLectura.java   # Modelo para lecturas
├── target/                       # Archivos compilados por Maven
├── .env                          # Variables de entorno para credenciales
├── pom.xml                       # Archivo de construcción Maven
└── lecturas\_sensor\_\*.csv         # Salidas CSV generadas

````

---

## ⚙️ Requisitos

- Java 17+
- Maven (`mvn`)

---

## 🔐 Configuración de Credenciales

Crear un archivo `.env` en la raíz del módulo con el siguiente contenido:

```env
THINGSBOARD_URL=http://localhost:8080
THINGSBOARD_USER=admin@urbia.local
THINGSBOARD_PASSWORD=sysadmin
````

> El archivo es leído automáticamente mediante la librería `dotenv-java`.

---

## 🛠️ Compilación y Ejecución

Este módulo **no utiliza `make`**. Usa directamente comandos de **Maven**:

### 1. Compilar el proyecto

```bash
mvn clean package
```

### 2. Ejecutar el cliente ThingsBoard

```bash
mvn exec:java
```

> También puedes usar:

```bash
mvn clean package exec:java
```

---

## 🧪 Ejemplo de Ejecución

```text
🌐 UrbIA :: Cliente Java para ThingsBoard

🧑 Usuario ThingsBoard: autenticando...
✅ Autenticación exitosa.

📋 Menú de opciones:
1) sensor_co2_urbia01 [default]
0) Salir

👉 Seleccione un dispositivo: 1

📈 Últimas lecturas de: sensor_co2_urbia01
📌 [2025-06-29 00:24:38] temperatura = 32.07
📌 [2025-06-29 00:24:38] co2 = 467.0
📌 [2025-06-29 00:24:38] humedad = 44.69

💾 ¿Desea exportar estas lecturas? (s/n): s
📁 Archivo CSV generado: lecturas_sensor_co2_urbia01.csv

👉 Seleccione un dispositivo: 0
👋 Programa finalizado.
```

---

## 📌 Clases Principales

| Clase               | Descripción                                     |
| ------------------- | ----------------------------------------------- |
| `Main`              | Interfaz principal (CLI interactivo)            |
| `ThingsBoardClient` | Cliente autenticado con lógica de conexión REST |
| `HttpUtils`         | Funciones auxiliares `GET` y `POST` HTTP        |
| `JsonUtils`         | Parseo seguro de JSON y transformación de datos |
| `SensorLectura`     | Clase que representa una lectura de sensor      |

---

## 📁 Archivos de Salida

* Se genera automáticamente un CSV:
  `lecturas_<nombre_dispositivo>.csv`
* Se guarda en el mismo directorio raíz del módulo.

---

