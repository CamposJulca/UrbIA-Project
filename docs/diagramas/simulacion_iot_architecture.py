from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Users
from diagrams.generic.device import Mobile
from diagrams.programming.language import Java, Python, Cpp
from diagrams.generic.os import Ubuntu

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
    "telemetria": {"color": "blue", "fontcolor": "blue"},
    "rest": {"color": "green", "fontcolor": "green"},
    "respuesta": {"color": "orange", "fontcolor": "orange"},
    "visual": {"color": "purple", "fontcolor": "purple"},
    "flujo": {"color": "black", "fontcolor": "black"},
}

with Diagram("Capa 2 - Simulación IoT (UrbIA - Fase 0)", show=True,
             filename="simulacion_iot_fase0", outformat="png", graph_attr=graph_attr):

    usuario = Users("Investigador / Autoridad\n(o Estudiante)")
    acceso = Mobile("Terminal o Navegador")

    usuario >> Edge(label="interacción", **edge_styles["visual"]) >> acceso

    with Cluster("Capa 2: Simulación IoT"):
        simulador_cpp = Cpp("Simulador de Sensores\n(C++)")
        gateway_java = Java("Cliente CLI\n(Java + REST)")
        cliente_python = Python("Dashboard Web\n(Streamlit + REST)")

    with Cluster("Capa 3: Plataforma IoT"):
        thingsboard = Ubuntu("ThingsBoard CE\n(instancia local)")

    # Flujo de datos
    simulador_cpp >> Edge(label="envía telemetría JSON", **edge_styles["telemetria"]) >> thingsboard
    gateway_java >> Edge(label="consulta series REST", **edge_styles["rest"]) >> thingsboard
    cliente_python >> Edge(label="consume API REST", **edge_styles["rest"]) >> thingsboard

    # Respuestas de ThingsBoard
    thingsboard >> Edge(label="respuesta JSON", **edge_styles["respuesta"]) >> gateway_java
    thingsboard >> Edge(label="respuesta JSON", **edge_styles["respuesta"]) >> cliente_python

    # Visualización hacia el usuario
    gateway_java >> Edge(label="salida consola\ntexto interactivo", **edge_styles["flujo"]) >> acceso
    cliente_python >> Edge(label="actualización visual web", **edge_styles["flujo"]) >> acceso
