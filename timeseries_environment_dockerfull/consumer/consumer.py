from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point, WritePrecision
from datetime import datetime
import json
from config import BROKER, TOPIC, INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[BROKER],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True,
)

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api()

print(f"Consuming from {BROKER} topic={TOPIC} → InfluxDB {INFLUX_URL}/{INFLUX_BUCKET}")
for msg in consumer:
    data = msg.value
    ts = data.get('ts')
    try:
        point = (
            Point("sensor_data")
            .tag("sensor", data.get("sensor", "sensor-1"))
            .field("value", float(data.get("value", 0)))
            .time(ts if ts else datetime.utcnow(), WritePrecision.NS)
        )
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        print("✓ inserted:", data)
    except Exception as e:
        print("⚠️ write error:", e, "payload:", data)