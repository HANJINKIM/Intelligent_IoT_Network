import os
from dotenv import load_dotenv
load_dotenv()

BROKER = f"{os.getenv('KAFKA_BROKER_HOST', 'localhost')}:{os.getenv('KAFKA_BROKER_PORT', '9092')}"
TOPIC = os.getenv('KAFKA_TOPIC', 'timeseries-topic')
INFLUX_URL = os.getenv('INFLUX_URL_HOST', 'http://localhost:8086')
INFLUX_TOKEN = os.getenv('INFLUX_ADMIN_TOKEN', 'admintoken')
INFLUX_ORG = os.getenv('INFLUX_ORG', 'myorg')
INFLUX_BUCKET = os.getenv('INFLUX_BUCKET', 'timeseries')