import pandas as pd
from influxdb_client import InfluxDBClient
import os
from dotenv import load_dotenv
load_dotenv()

URL = os.getenv('INFLUX_URL_HOST', 'http://localhost:8086')
TOKEN = os.getenv('INFLUX_ADMIN_TOKEN', 'admintoken')
ORG = os.getenv('INFLUX_ORG', 'myorg')
BUCKET = os.getenv('INFLUX_BUCKET', 'timeseries')

QUERY_TEMPLATE = """
from(bucket: \"%s\")
  |> range(start: %s)
  |> filter(fn: (r) => r._measurement == \"sensor_data\")
  |> filter(fn: (r) => r._field == \"value\")
  |> keep(columns: [\"_time\", \"_value\", \"sensor\"])
  |> sort(columns:[\"_time\"])
"""

def load_series(range_start='-6h'):
    query = QUERY_TEMPLATE % (BUCKET, range_start)
    with InfluxDBClient(url=URL, token=TOKEN, org=ORG) as client:
        df = client.query_api().query_data_frame(query)
    if isinstance(df, list):
        df = pd.concat(df, ignore_index=True)
    df = df.rename(columns={"_time":"time","_value":"value"})
    df = df[["time","value"]].dropna()
    return df