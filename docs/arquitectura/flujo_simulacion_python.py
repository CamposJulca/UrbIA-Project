from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.monitoring import Prometheus
from diagrams.programming.language import Python
from diagrams.programming.flowchart import InputOutput, PredefinedProcess
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.analytics import Tableau
from diagrams.generic.storage import Storage
from diagrams.generic.network import Firewall

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
    "visual": {"color": "darkgreen", "fontcolor": "darkgreen"},
    "almacenamiento": {"color": "purple", "fontcolor": "purple"},
}

with Diagram("Flujo Interno - Cliente Python (UrbIA Fase 0)", show=True,
             filename="flujo_simulador_python", outformat="png", graph_attr=graph_attr):

    with Cluster("ThingsBoard Server"):
        api_tb = InputOutput("API\n/telemetry")

    with Cluster("Cliente Python"):
        http_cliente = Python("HTTP\nGET JSON")
        parser = PredefinedProcess("Parser\ny limpieza")
        actualizador = PredefinedProcess("Actualizar\ndatos internos")

    with Cluster("Visualización"):
        streamlit = Tableau("Streamlit\nDashboard")

    with Cluster("Persistencia local"):
        db = PostgreSQL("PostgreSQL\nlocal")
        archivos = Storage("Exportar CSV")

    with Cluster("Auditoría"):
        logger = Storage("Logs")

    api_tb >> Edge(label="GET JSON", **edge_styles["http"]) >> http_cliente
    http_cliente >> Edge(label="procesa datos", **edge_styles["flujo"]) >> parser
    parser >> Edge(label="estructura", **edge_styles["flujo"]) >> actualizador
    actualizador >> Edge(label="muestra", **edge_styles["visual"]) >> streamlit
    actualizador >> Edge(label="guarda", **edge_styles["almacenamiento"]) >> db
    actualizador >> Edge(label="exporta", **edge_styles["almacenamiento"]) >> archivos

    http_cliente >> Edge(label="registro", **edge_styles["log"]) >> logger
