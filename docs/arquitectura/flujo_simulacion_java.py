from diagrams import Diagram, Cluster, Edge
from diagrams.programming.language import Java
from diagrams.programming.flowchart import PredefinedProcess, InputOutput
from diagrams.generic.device import Mobile
from diagrams.generic.storage import Storage
from diagrams.onprem.client import Users
from diagrams.custom import Custom

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
    "estructura": {"color": "green", "fontcolor": "green"},
    "modelo": {"color": "gray", "fontcolor": "gray"},
    "visual": {"color": "purple", "fontcolor": "purple"},
}

with Diagram("Flujo Interno - Gateway Java (UrbIA Fase 0)", show=False,
             filename="flujo_gateway_java_mejorado", outformat="png", graph_attr=graph_attr):

    with Cluster("Gateway Java CLI", graph_attr={"style": "filled", "color": "#f0f8ff"}):
        main_menu = Java("Main.java\nCLI Menú")
        client = PredefinedProcess("ThingsBoardClient.java\n(Auth + REST)")
        http = PredefinedProcess("HttpUtils.java\n(Peticiones HTTP)")
        json = PredefinedProcess("JsonUtils.java\n(JSON Parsing)")
        model = PredefinedProcess("SensorLectura.java\n(Modelo de Datos)")

        main_menu >> Edge(label="invoca cliente", **edge_styles["flujo"]) >> client
        client >> Edge(label="usa", **edge_styles["flujo"]) >> http
        client >> Edge(label="estructura datos", **edge_styles["estructura"]) >> json
        json >> Edge(label="modelo de lectura", **edge_styles["modelo"]) >> model

    with Cluster("ThingsBoard Server"):
        api = InputOutput("API\n/telemetry")

    with Cluster("Salida / Exportación"):
        cli_out = Users("Visualización\npor consola")
        export_csv = Storage("Exportar CSV")

    with Cluster("Auditoría"):
        logs = Storage("Logs")

    http >> Edge(label="GET JSON", **edge_styles["http"]) >> api
    client >> Edge(label="muestra CLI", **edge_styles["visual"]) >> cli_out
    client >> Edge(label="exporta CSV", **edge_styles["visual"]) >> export_csv
    http >> Edge(label="registro", **edge_styles["modelo"]) >> logs
    main_menu >> Edge(label="log ejecución", **edge_styles["modelo"]) >> logs
