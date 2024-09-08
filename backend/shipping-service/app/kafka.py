import threading
from kafka import KafkaConsumer, KafkaProducer
import json
from app.app_config import AppConfig
from app.shipping_service import handle_order_printed_event


def kafka_consumer_loop(consumer):
    for message in consumer:
        try:
            print(f"Received printed order: {message.value}")
            handle_order_printed_event(message.value)
        except Exception as e:
            print(f"Error in kafka_consumer_loop: {e}")

def start_kafka_consumer():
    consumer = KafkaConsumer(
        "order_printed",
        bootstrap_servers=AppConfig.KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    consumer_thread = threading.Thread(target=kafka_consumer_loop, args=(consumer,))
    consumer_thread.start()
    print("Kafka consumer started.")
    return consumer, consumer_thread

def stop_kafka_consumer(consumer, consumer_thread):
    if consumer:
        consumer.close()
        print("Kafka consumer closed.")
    if consumer_thread:
        consumer_thread.join()
        print("Kafka consumer thread joined.")

def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=AppConfig.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
