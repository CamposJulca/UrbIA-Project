# dashboard.py

import streamlit as st
import pandas as pd
import time
import altair as alt
from core.api import autenticar_tenant, obtener_dispositivos, obtener_telemetria_historica

# Configuración
st.set_page_config(page_title="Dashboard UrbIA - Sensores en Tiempo Real", layout="wide")
st.title("🌡️ Dashboard UrbIA - Sensores en Tiempo Real")

# Auto-refresh (toggle)
auto_refresh = st.sidebar.checkbox("🔄 Auto-actualizar cada 60s")
if auto_refresh:
    time.sleep(60)
    st.experimental_rerun()

# Paso 1: Autenticación
st.write("🔐 Autenticando con ThingsBoard...")
token = autenticar_tenant()
if token:
    st.success("✅ Token JWT recibido")
    print(f"✅ Token recibido: {token}")
else:
    st.error("❌ No se pudo autenticar con ThingsBoard")
    st.stop()

# Paso 2: Obtener sensores
st.write("📡 Solicitando lista de dispositivos...")
dispositivos = obtener_dispositivos(token)
if not dispositivos:
    st.warning("⚠️ No se encontraron dispositivos.")
    st.stop()

opciones = {d["name"]: d["id"]["id"] for d in dispositivos}
dispositivo_nombre = st.selectbox("Selecciona un sensor:", list(opciones.keys()))
dispositivo_id = opciones[dispositivo_nombre]
st.success(f"✅ Datos cargados para {dispositivo_nombre}")
print(f"📌 Sensor seleccionado: {dispositivo_nombre} ({dispositivo_id})")

# Paso 3: Selección de variables
todas_las_keys = ["temperatura", "humedad", "co2", "presion", "luz", "ruido"]
variables_seleccionadas = st.multiselect("📌 Selecciona variables a visualizar:", todas_las_keys, default=todas_las_keys)

# Paso 4: Filtro de tiempo
rango_minutos = st.slider("🕒 Rango de tiempo (minutos atrás)", min_value=5, max_value=180, value=10, step=5)

# Paso 5: Obtener telemetría
print(f"📥 Solicitando telemetría de los últimos {rango_minutos} minutos para: {','.join(variables_seleccionadas)}")
df = obtener_telemetria_historica(dispositivo_id, token, variables_seleccionadas, minutos=rango_minutos)

if not isinstance(df, pd.DataFrame) or df.empty:
    st.warning("⚠️ No se encontraron datos.")
    st.stop()

print(f"✅ Telemetría recibida con {df['sensor'].nunique()} variables y {len(df)} filas.")

# Paso 6: Mostrar KPIs actuales
st.markdown("### 🧭 Indicadores actuales por variable")
últimos_valores = df.sort_values("timestamp").groupby("sensor").tail(1).set_index("sensor")
kpi_cols = st.columns(len(últimos_valores))
for i, (sensor, row) in enumerate(últimos_valores.iterrows()):
    kpi_cols[i].metric(label=sensor.capitalize(), value=f"{row['valor']:.2f}")

# Paso 7: Tabla de datos
st.markdown("### 📊 Datos obtenidos (últimos registros)")
st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)

# Paso 8: Visualización
st.markdown("### 📈 Gráfica por variable")
chart = alt.Chart(df).mark_line().encode(
    x=alt.X('timestamp:T', title='Fecha y Hora'),
    y=alt.Y('valor:Q', title='Valor'),
    color=alt.Color('sensor:N', title='Variable medida')
).properties(
    title=f"Evolución de variables medidas - {dispositivo_nombre}",
    width=1100,
    height=400
).interactive()
st.altair_chart(chart, use_container_width=True)

# Paso 9: Estadísticas resumen
st.markdown("### 📌 Estadísticas por variable")
resumen = df.groupby("sensor")["valor"].agg(['mean', 'min', 'max']).reset_index()
resumen.columns = ['Sensor', 'Promedio', 'Mínimo', 'Máximo']
st.table(resumen.style.format({"Promedio": "{:.2f}", "Mínimo": "{:.2f}", "Máximo": "{:.2f}"}))

print("📊 Estadísticas calculadas por variable:")
print(resumen)

# Paso 10: Botón de exportación
st.markdown("### 📁 Exportar datos")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="📥 Descargar CSV", data=csv, file_name="telemetria_urbia.csv", mime='text/csv')

# # dashboard.py

# import streamlit as st
# import pandas as pd
# import altair as alt
# from client import ThingsBoardClient
# from utils.refresh import manejar_auto_actualizacion
# from utils.kpis import mostrar_kpis
# from utils.table import mostrar_tabla
# from utils.graph import graficar
# from utils.stats import mostrar_resumen_estadistico
# from utils.download import descargar_csv

# # Configuración de la página
# st.set_page_config(page_title="Dashboard UrbIA - Sensores en Tiempo Real", layout="wide")
# st.title("🌡️ Dashboard UrbIA - Sensores en Tiempo Real")

# # Auto-refresh con opción toggle
# auto_refresh = st.sidebar.checkbox("🔄 Auto-actualizar cada 60s")
# manejar_auto_actualizacion(auto_refresh)

# # Inicializar cliente
# client = ThingsBoardClient()
# token = client.autenticar()
# if not token:
#     st.error("❌ No se pudo autenticar con ThingsBoard")
#     st.stop()

# dispositivos = client.obtener_dispositivos(token)
# if not dispositivos:
#     st.warning("⚠️ No se encontraron dispositivos.")
#     st.stop()

# opciones = {d["name"]: d["id"]["id"] for d in dispositivos}
# dispositivo_nombre = st.selectbox("Selecciona un sensor:", list(opciones.keys()))
# dispositivo_id = opciones[dispositivo_nombre]
# st.success(f"✅ Datos cargados para {dispositivo_nombre}")

# # Selección de variables y tiempo
# todas_las_keys = ["temperatura", "humedad", "co2", "presion", "luz", "ruido"]
# variables_seleccionadas = st.multiselect("📌 Selecciona variables a visualizar:", todas_las_keys, default=todas_las_keys)
# rango_minutos = st.slider("🕒 Rango de tiempo (minutos atrás)", min_value=5, max_value=180, value=10, step=5)

# # Obtener telemetría
# df = client.obtener_telemetria_historica(dispositivo_id, token, variables_seleccionadas, minutos=rango_minutos)
# if df.empty:
#     st.warning("⚠️ No se encontraron datos.")
#     st.stop()

# # Visualizaciones
# mostrar_kpis(df)
# mostrar_tabla(df)
# graficar(df, dispositivo_nombre)
# mostrar_resumen_estadistico(df)
# descargar_csv(df)
