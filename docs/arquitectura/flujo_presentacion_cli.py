from diagrams import Diagram, Cluster, Edge
from diagrams.programming.language import Java
from diagrams.onprem.client import Users
from diagrams.generic.compute import Rack
from diagrams.generic.network import Firewall
from diagrams.generic.storage import Storage
from diagrams.generic.os import Ubuntu
from diagrams.programming.flowchart import InputOutput, PredefinedProcess

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

with Diagram("Flujo Interno - Cliente CLI Java (UrbIA Fase 0)", show=True,
             filename="flujo_presentacion_cli", outformat="png", graph_attr=graph_attr):

    usuario = Users("Usuario (Terminal)")

    with Cluster("CLI Java (presentacion_cli)"):
        main = Java("Main.java")
        auth = PredefinedProcess("AuthService\nAutenticación")
        menu = PredefinedProcess("MenuController\nMenú dinámico")

        with Cluster("Servicios REST"):
            device_service = PredefinedProcess("DeviceService\nConsultar dispositivos")
            telemetry_service = PredefinedProcess("TelemetryService\nConsultar telemetría")

        with Cluster("Procesamiento"):
            parser = PredefinedProcess("JsonUtils\nParsear JSON")
            formatter = PredefinedProcess("DateFormatter\nFormatear timestamp")

        exportar = PredefinedProcess("CsvExporter\nExportar a CSV")

    with Cluster("ThingsBoard"):
        api_login = InputOutput("/auth/login")
        api_telemetry = InputOutput("/telemetry")
        api_devices = InputOutput("/devices")

    archivo_csv = Storage("Archivo CSV\n(local)")
    logs = Storage("Consola / Logs")

    # Flujo principal
    usuario >> Edge(label="ejecuta", **edge_styles["interaccion"]) >> main
    main >> auth >> api_login
    main >> menu >> device_service >> api_devices
    menu >> telemetry_service >> api_telemetry
    telemetry_service >> parser >> formatter
    formatter >> Edge(label="muestra lecturas", **edge_styles["interaccion"]) >> usuario
    formatter >> Edge(label="opción exportar", **edge_styles["export"]) >> exportar >> archivo_csv
    exportar >> Edge(label="registro", **edge_styles["log"]) >> logs
