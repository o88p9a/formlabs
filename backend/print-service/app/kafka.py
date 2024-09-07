import threading

from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
from app.database import SessionLocal
from app.models import PrintOrder, PrintOrderItem
from app.app_config import AppConfig


def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=AppConfig.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

consumer = KafkaConsumer(
    "order",
    bootstrap_servers=AppConfig.KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode('ascii'))
)

# Process incoming orders from Kafka
def process_order(order_data):
    db = SessionLocal()

    print_order = PrintOrder(
        id=order_data['id'],
        customer_id=order_data['customer_id'],
        customer_name=order_data['customer_name'],
        status='pending'
    )

    for item in order_data['items']:
        print_order_item = PrintOrderItem(
            sample_part_id=item['sample_part_id'],
            material_id=item['material_id'],
            quantity=item['quantity'],
            order=print_order
        )
        db.add(print_order_item)

    db.add(print_order)
    db.commit()
    db.close()

def kafka_consumer_loop():
    global consumer
    for message in consumer:
        order_data = message.value
        process_order(order_data)

def start_kafka_consumer():
    global consumer, consumer_thread
    consumer = KafkaConsumer(
        "order",
        bootstrap_servers=AppConfig.KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('ascii'))
    )
    consumer_thread = threading.Thread(target=kafka_consumer_loop)
    consumer_thread.start()

def stop_kafka_consumer():
    global consumer, consumer_thread
    if consumer:
        consumer.close()
    if consumer_thread:
        consumer_thread.join()
