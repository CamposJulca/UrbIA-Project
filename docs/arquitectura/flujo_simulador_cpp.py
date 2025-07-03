from diagrams import Diagram, Cluster, Edge
from diagrams.generic.compute import Rack
from diagrams.onprem.client import Users
from diagrams.programming.language import Cpp
from diagrams.programming.flowchart import InputOutput, PredefinedProcess
from diagrams.generic.storage import Storage

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
    "json": {"color": "darkgreen", "fontcolor": "darkgreen"},
    "http": {"color": "blue", "fontcolor": "blue"},
    "log": {"color": "gray", "fontcolor": "gray", "style": "dashed"},
}

with Diagram("Flujo Interno - Simulador C++ (UrbIA Fase 0)", show=True,
             filename="flujo_simulador_cpp_v2", outformat="png", graph_attr=graph_attr):

    with Cluster("Simulación"):
        sensores = Cpp("Sensor*.cpp\n(virtuales)")
        json_builder = PredefinedProcess("JsonBuilder")
        cliente_http = Rack("HttpClient\n(libcurl)")

    with Cluster("ThingsBoard Local"):
        endpoint = InputOutput("POST\n/api/v1/<token>/telemetry")

    with Cluster("Logs"):
        log_consola = Users("Log\nconsola")
        log_archivo = Storage("Log\nsimulador.log")

    sensores >> Edge(label="lecturas", **edge_styles["flujo"]) >> json_builder
    json_builder >> Edge(label="genera JSON", **edge_styles["json"]) >> cliente_http
    cliente_http >> Edge(label="POST\n(cada 5s)", **edge_styles["http"]) >> endpoint

    json_builder >> Edge(label="registro", **edge_styles["log"]) >> log_consola
    cliente_http >> Edge(label="confirmación", **edge_styles["log"]) >> log_archivo
