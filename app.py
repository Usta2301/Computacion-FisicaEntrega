# app.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from src.influx_helpers import obtener_dht22, obtener_mpu6050

# --------------------------
# Configuración Streamlit
# --------------------------
st.set_page_config(page_title="IoT Dashboard Avanzado", layout="wide")
st.markdown("<h1 style='text-align:center;'>🌿 IoT Dashboard - Monitoreo Ambiental y Movimiento</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar - filtros
st.sidebar.header("Filtros de visualización")
tiempo_actual = datetime.now()
fecha_inicio = st.sidebar.date_input("Fecha inicio", tiempo_actual - timedelta(days=1))
fecha_fin = st.sidebar.date_input("Fecha fin", tiempo_actual)
actualizar = st.sidebar.button("Actualizar datos")

# --------------------------
# Función para mostrar tarjetas con colores según rango
# --------------------------
def tarjeta_valor(titulo, valor, unidad, min_val=None, max_val=None):
    color = "#90EE90"  # verde por defecto
    if min_val is not None and valor < min_val:
        color = "#FFA07A"  # rojo claro
    if max_val is not None and valor > max_val:
        color = "#FF4500"  # rojo intenso
    st.markdown(f"""
        <div style="background-color:{color};padding:15px;border-radius:10px;text-align:center">
            <h3>{titulo}</h3>
            <h2>{valor:.2f} {unidad}</h2>
        </div>
        """, unsafe_allow_html=True)

# --------------------------
# Mostrar datos
# --------------------------
if actualizar:
    try:
        # Obtener datos desde InfluxDB
        dht22_data = obtener_dht22(fecha_inicio, fecha_fin)
        mpu6050_data = obtener_mpu6050(fecha_inicio, fecha_fin)

        # ---- DHT22 ----
        if not dht22_data.empty:
            st.subheader("🌡️ Temperatura y Humedad (DHT22)")
            fig_temp = px.line(dht22_data, x="_time", y="temperature", title="Temperatura (°C)", markers=True)
            fig_hum = px.line(dht22_data, x="_time", y="humidity", title="Humedad (%)", markers=True)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig_temp, use_container_width=True)
            col2.plotly_chart(fig_hum, use_container_width=True)

            # Tarjetas de temperatura y humedad actuales
            col1, col2 = st.columns(2)
            tarjeta_valor("Temperatura Actual", dht22_data['temperature'].iloc[-1], "°C", min_val=15, max_val=30)
            tarjeta_valor("Humedad Actual", dht22_data['humidity'].iloc[-1], "%", min_val=30, max_val=70)
        else:
            st.warning("No hay datos de DHT22 para las fechas seleccionadas.")

        # ---- MPU6050 ----
        if not mpu6050_data.empty:
            st.subheader("🌀 Movimiento (MPU6050)")
            fig_acc = px.line(mpu6050_data, x="_time", y=["acc_x","acc_y","acc_z"], title="Aceleración (m/s²)", markers=True)
            st.plotly_chart(fig_acc, use_container_width=True)

            # Tarjetas aceleración actuales
            col1, col2, col3 = st.columns(3)
            tarjeta_valor("Acc X", mpu6050_data['acc_x'].iloc[-1], "m/s²", max_val=2)
            tarjeta_valor("Acc Y", mpu6050_data['acc_y'].iloc[-1], "m/s²", max_val=2)
            tarjeta_valor("Acc Z", mpu6050_data['acc_z'].iloc[-1], "m/s²", max_val=2)
        else:
            st.warning("No hay datos de MPU6050 para las fechas seleccionadas.")

    except Exception as e:
        st.error(f"Error al obtener datos desde InfluxDB: {e}")

else:
    st.info("Seleccione la fecha y presione 'Actualizar datos'.")
