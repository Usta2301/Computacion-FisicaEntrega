import pandas as pd
from influxdb_client import InfluxDBClient

# --------------------------
# Configuración de InfluxDB
# --------------------------
INFLUX_URL = "https://tu-influxdb-url.com"
INFLUX_TOKEN = "TU_TOKEN_AQUI"
INFLUX_ORG = "TU_ORG"
INFLUX_BUCKET = "TU_BUCKET"

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()

# Función para obtener datos del sensor DHT22
def obtener_dht22(fecha_inicio, fecha_fin):
    query = f'''
    from(bucket:"{INFLUX_BUCKET}")
    |> range(start: {fecha_inicio.isoformat()}T00:00:00Z, stop: {fecha_fin.isoformat()}T23:59:59Z)
    |> filter(fn: (r) => r["_measurement"] == "DHT22")
    '''
    result = query_api.query_data_frame(query)
    if not result.empty:
        df = result[["_time", "_field", "_value"]].pivot(index="_time", columns="_field", values="_value")
        df = df.reset_index()
        return df
    return pd.DataFrame()

# Función para obtener datos del sensor MPU6050
def obtener_mpu6050(fecha_inicio, fecha_fin):
    query = f'''
    from(bucket:"{INFLUX_BUCKET}")
    |> range(start: {fecha_inicio.isoformat()}T00:00:00Z, stop: {fecha_fin.isoformat()}T23:59:59Z)
    |> filter(fn: (r) => r["_measurement"] == "MPU6050")
    '''
    result = query_api.query_data_frame(query)
    if not result.empty:
        df = result[["_time", "_field", "_value"]].pivot(index="_time", columns="_field", values="_value")
        df = df.reset_index()
        return df
    return pd.DataFrame()

