from kafka import KafkaProducer
import json, time, random
from datetime import datetime, timezone
from config import BROKER, TOPIC, SENSOR_ID, INTERVAL_SEC

producer = KafkaProducer(
    bootstrap_servers=[BROKER],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

print(f"Producing to {BROKER} topic={TOPIC} ... Ctrl+C to stop")
while True:
    payload = {
        "sensor": SENSOR_ID,
        "value": round(random.uniform(20.0, 30.0), 3),
        "ts": datetime.now(timezone.utc).isoformat()
    }
    producer.send(TOPIC, payload)
    print("→", payload)
    time.sleep(INTERVAL_SEC)