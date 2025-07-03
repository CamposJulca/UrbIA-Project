from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.analytics import Spark
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.programming.language import Python
from diagrams.generic.storage import Storage
from diagrams.generic.os import Ubuntu
from diagrams.programming.flowchart import PredefinedProcess, InputOutput
from diagrams.custom import Custom

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
    "lecturas": {"color": "orange", "fontcolor": "orange"},
    "procesamiento": {"color": "blue", "fontcolor": "blue"},
    "resultado": {"color": "green", "fontcolor": "green"},
    "log": {"color": "gray", "style": "dashed"},
}

with Diagram("Capa 5 - Procesamiento Analítico (UrbIA Fase 0)", show=True,
             filename="flujo_capa5_spark", outformat="png", graph_attr=graph_attr):

    with Cluster("Entorno Local (Ubuntu)", graph_attr={"bgcolor": "#f9f9f9"}):
        sistema = Ubuntu("Ubuntu Desktop")
        sqlite = Redis("edge_data.db\n(SQLite)")
        postgres = PostgreSQL("PostgreSQL\n(opcional)")

        with Cluster("Módulo procesamiento_spark"):
            run_script = Python("run_job.sh")
            main_pipeline = Python("jobs.py\n(Pipeline Spark)")
            config_loader = Python("settings.py")
            log_files = Storage("logs/\n*.log")
            timer = Python("timer.py")
            syncer = Python("sync_sqlite.py")

        with Cluster("Módulo servicios"):
            db_sqlite = Python("db_sqlite.py")
            db_postgres = Python("db_postgres.py")

        with Cluster("Resultados"):
            csv_output = Storage("metricas_agg.csv")
            graficos = Storage("gráficos\n(sensor-XYZ.png)")
            visualizador = Python("visualizar_metricas.py")

    # Flujo
    sistema >> run_script >> main_pipeline

    main_pipeline >> Edge(label="lee lecturas", **edge_styles["lecturas"]) >> db_sqlite >> sqlite

    main_pipeline >> Edge(label="procesa Spark", **edge_styles["procesamiento"]) >> [csv_output, graficos]
    main_pipeline >> Edge(label="escribe (opcional)", **edge_styles["procesamiento"]) >> db_postgres >> postgres

    visualizador >> Edge(label="lee métricas", **edge_styles["resultado"]) >> csv_output

    [main_pipeline, db_sqlite, db_postgres] >> Edge(label="usa configuración", **edge_styles["procesamiento"]) >> config_loader
    main_pipeline >> Edge(label="sincroniza", **edge_styles["procesamiento"]) >> syncer
    main_pipeline >> Edge(label="mide tiempos", **edge_styles["procesamiento"]) >> timer
    main_pipeline >> Edge(label="genera logs", **edge_styles["log"]) >> log_files
