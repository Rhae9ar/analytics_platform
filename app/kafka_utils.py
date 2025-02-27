from kafka import KafkaProducer
from .models import Event
import json
from dotenv import load_dotenv
import os

load_dotenv()

KAFKA_HOST = os.getenv("KAFKA_HOST")

producer = KafkaProducer(bootstrap_servers=KAFKA_HOST, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_event(event: Event):
    """Отправка события в Kafka."""
    producer.send('events', event.dict())