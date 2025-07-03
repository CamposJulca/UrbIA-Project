from diagrams import Diagram, Cluster, Edge
from diagrams.programming.language import Python, Javascript
from diagrams.onprem.client import Users
from diagrams.onprem.container import Docker
from diagrams.generic.network import Firewall
from diagrams.generic.storage import Storage
from diagrams.programming.flowchart import InputOutput, PredefinedProcess
from diagrams.onprem.monitoring import Prometheus

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "layout": "dot",
    "splines": "polyline",
    "rankdir": "LR",
    "ranksep": "0.75",
    "nodesep": "0.6",
}

edge_styles = {
    "flujo": {"color": "black", "fontcolor": "black"},
    "http": {"color": "blue", "fontcolor": "blue"},
    "log": {"color": "gray", "fontcolor": "gray", "style": "dashed"},
    "export": {"color": "purple", "fontcolor": "purple"},
    "interaccion": {"color": "darkgreen", "fontcolor": "darkgreen"},
}

with Diagram("Arquitectura Interna - presentacion_web (UrbIA Fase 0)", show=False,
             filename="arquitectura_presentacion_web", outformat="png", graph_attr=graph_attr):

    usuario = Users("Usuario\n(Navegador)")

    with Cluster("Frontend React (Vite)"):
        interfaz = Javascript("DevicesPage.jsx\nVista principal")
        sensor_card = PredefinedProcess("SensorCard.jsx\nComponente por sensor")

    with Cluster("Backend FastAPI"):
        fastapi = Python("main.py")
        config = PredefinedProcess("Config\n(.env / config.py)")
        router = PredefinedProcess("Rutas\n(api/endpoints)")
        client = PredefinedProcess("ThingsBoardClient\nAuth y fetch")

    with Cluster("ThingsBoard API"):
        api_login = InputOutput("/auth/login")
        api_devices = InputOutput("/devices")
        api_telemetry = InputOutput("/telemetry")

    archivo_log = Storage("Logs")
    panel_docs = InputOutput("/docs")

    # Interacción usuario
    usuario >> Edge(label="carga interfaz", **edge_styles["interaccion"]) >> interfaz
    interfaz >> Edge(label="muestra sensores", **edge_styles["interaccion"]) >> sensor_card

    # Comunicación frontend-backend
    interfaz >> Edge(label="GET /api/devices", **edge_styles["http"]) >> fastapi
    fastapi >> config
    fastapi >> router >> client

    # Comunicación backend - ThingsBoard
    client >> api_login
    client >> api_devices
    client >> api_telemetry

    # Respuesta a frontend
    client >> Edge(label="datos sensores", **edge_styles["http"]) >> interfaz

    # Logs y documentación
    fastapi >> Edge(label="docs auto", **edge_styles["log"]) >> panel_docs
    fastapi >> Edge(label="registro", **edge_styles["log"]) >> archivo_log
