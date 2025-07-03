from diagrams import Diagram, Cluster, Edge
from diagrams.programming.language import Cpp, Python
from diagrams.onprem.client import Users
from diagrams.generic.compute import Rack
from diagrams.generic.network import Firewall
from diagrams.generic.storage import Storage
from diagrams.onprem.database import PostgreSQL
from diagrams.generic.os import Ubuntu
from diagrams.programming.flowchart import PredefinedProcess, InputOutput
from diagrams.onprem.monitoring import Prometheus

graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "layout": "dot",
    "splines": "polyline",
    "rankdir": "LR",
    "ranksep": "0.8",
    "nodesep": "0.6",
}

edge_styles = {
    "telemetria": {"color": "red", "fontcolor": "red"},
    "consulta": {"color": "blue", "fontcolor": "blue"},
    "dashboard": {"color": "green", "fontcolor": "green"},
    "bd": {"color": "gray", "style": "dashed"},
}

with Diagram("Capa 3 - ThingsBoard (UrbIA Fase 0)", show=True,
             filename="flujo_capa3_thingsboard", outformat="png", graph_attr=graph_attr):

    usuario = Users("Usuario Final")

    with Cluster("Simuladores"):
        simulador_cpp = Cpp("simulador_cpp\n(en C++)")
        simulacion_python = Python("simulacion_python\n(Streamlit)")
        simulacion_gateway = Python("simulacion_gateway\n(CLI Python)")

    with Cluster("Servidor ThingsBoard", graph_attr={"bgcolor": "#f9f9f9"}):
        ubuntu_server = Ubuntu("Ubuntu Server\n(local)")
        firewall = Firewall("Puerto 8080 abierto")
        with Cluster("ThingsBoard", graph_attr={"bgcolor": "#e0f7fa"}):
            auth_api = InputOutput("Auth API")
            telemetry_api = InputOutput("Telemetry API")
            device_api = InputOutput("Device API")
            dashboard = PredefinedProcess("Visualización\nDashboards")
            tb_postgres = PostgreSQL("tb_postgres")

    # Conexiones
    simulador_cpp >> Edge(label="envía telemetría", **edge_styles["telemetria"]) >> telemetry_api
    telemetry_api >> Edge(label="almacena", **edge_styles["bd"]) >> tb_postgres

    simulacion_python >> Edge(label="consulta dispositivos", **edge_styles["consulta"]) >> device_api
    simulacion_python >> Edge(label="consulta telemetría", **edge_styles["consulta"]) >> telemetry_api

    simulacion_gateway >> Edge(label="consulta telemetría", **edge_styles["consulta"]) >> telemetry_api

    usuario >> Edge(label="accede a dashboard", **edge_styles["dashboard"]) >> dashboard
    dashboard >> telemetry_api
    dashboard >> device_api

    ubuntu_server >> firewall >> [auth_api, telemetry_api, device_api, dashboard]
