import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main(csv_path: str, output_dir: str):
    if not os.path.exists(csv_path):
        print(f"❌ No se encontró el archivo CSV: {csv_path}")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.read_csv(csv_path)
    print(f"✅ CSV cargado con {len(df)} registros")
    print(df.head())

    for sensor_id in df["sensor_id"].unique():
        df_sensor = df[df["sensor_id"] == sensor_id]

        tipos = df_sensor["tipo"].tolist()
        promedios = df_sensor["promedio"].tolist()
        minimos = df_sensor["minimo"].tolist()
        maximos = df_sensor["maximo"].tolist()

        x = np.arange(len(tipos))
        width = 0.4

        fig, ax = plt.subplots(figsize=(10, 6))

        # Barra para promedio
        ax.bar(x, promedios, width, label='Promedio', color='skyblue')

        # Puntos para mínimo y máximo
        ax.scatter(x, minimos, color='red', marker='o', label='Mínimo', zorder=5)
        ax.scatter(x, maximos, color='green', marker='o', label='Máximo', zorder=5)

        # (Opcional) líneas verticales entre min y max
        for xi, mini, maxi in zip(x, minimos, maximos):
            ax.vlines(xi, mini, maxi, color='gray', linestyles='dashed', alpha=0.5)

        ax.set_xlabel("Tipo de variable")
        ax.set_ylabel("Valor")
        ax.set_title(f"Métricas por tipo - {sensor_id}")
        ax.set_xticks(x)
        ax.set_xticklabels(tipos)
        ax.legend()
        plt.tight_layout()

        output_path = os.path.join(output_dir, f"grafico_sensor_{sensor_id}.png")
        plt.savefig(output_path)
        plt.close()
        print(f"📊 Gráfico guardado: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("❌ Uso incorrecto. Ejemplo:\n   python scripts/visualizar_metricas.py path/a/metricas.csv path/a/carpeta_salida")
    else:
        csv_path = sys.argv[1]
        output_dir = sys.argv[2]
        main(csv_path, output_dir)
