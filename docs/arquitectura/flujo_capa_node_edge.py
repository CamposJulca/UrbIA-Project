from diagrams import Diagram, Cluster, Edge
from diagrams.programming.language import Python
from diagrams.generic.compute import Rack
from diagrams.onprem.client import Users
from diagrams.onprem.database import PostgreSQL
from diagrams.generic.os import Ubuntu
from diagrams.programming.flowchart import InputOutput, PredefinedProcess
from diagrams.onprem.analytics import Spark

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
    "procesamiento": {"color": "purple", "fontcolor": "purple"},
    "consulta": {"color": "blue", "fontcolor": "blue"},
    "bd": {"color": "gray", "style": "dashed"},
}

with Diagram("Capa 4 - Nodo Edge (UrbIA Fase 0)", show=True,
             filename="flujo_capa4_nodo_edge", outformat="png", graph_attr=graph_attr):

    usuario = Users("Investigador /\nDesarrollador")

    with Cluster("Simulador IoT", graph_attr={"bgcolor": "#fef9f9"}):
        simulador = Python("enviar_lecturas.py\n(Stream de datos)")

    with Cluster("Nodo Edge (FastAPI)", graph_attr={"bgcolor": "#e8f5e9"}):
        fastapi_srv = Python("FastAPI\n(app/main.py)")

        with Cluster("Módulos Internos", graph_attr={"bgcolor": "#f3e5f5"}):
            endpoint_telemetria = InputOutput("POST /api/telemetria")
            endpoint_procesar = InputOutput("POST /api/procesar-lote")
            endpoint_lecturas = InputOutput("GET /api/lecturas")
            endpoint_resumen = InputOutput("GET /api/resumen")
            procesamiento = PredefinedProcess("Procesamiento\npor lote (batch.py)")

    with Cluster("Persistencia Local", graph_attr={"bgcolor": "#eeeeee"}):
        sqlite = PostgreSQL("SQLite\n(edge_data.db)")

    # Conexiones
    usuario >> Edge(label="consulta\nresultados", **edge_styles["consulta"]) >> endpoint_lecturas
    usuario >> Edge(label="consulta resumen", **edge_styles["consulta"]) >> endpoint_resumen

    simulador >> Edge(label="envía telemetría", **edge_styles["telemetria"]) >> endpoint_telemetria
    endpoint_telemetria >> Edge(label="inserta", **edge_styles["bd"]) >> sqlite

    endpoint_procesar >> Edge(label="llama", **edge_styles["procesamiento"]) >> procesamiento
    procesamiento >> Edge(label="resume y guarda", **edge_styles["bd"]) >> sqlite

    endpoint_lecturas >> Edge(label="consulta", **edge_styles["bd"]) >> sqlite
    endpoint_resumen >> Edge(label="consulta", **edge_styles["bd"]) >> sqlite
