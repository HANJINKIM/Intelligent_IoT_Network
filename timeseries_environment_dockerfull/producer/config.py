import os
from dotenv import load_dotenv
load_dotenv()

BROKER = f"{os.getenv('KAFKA_BROKER_HOST', 'localhost')}:{os.getenv('KAFKA_BROKER_PORT', '9092')}"
TOPIC = os.getenv('KAFKA_TOPIC', 'timeseries-topic')
SENSOR_ID = os.getenv('SENSOR_ID', 'sensor-1')
INTERVAL_SEC = float(os.getenv('INTERVAL_SEC', '1.0'))