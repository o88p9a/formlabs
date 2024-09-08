import threading
from kafka import KafkaConsumer, KafkaProducer
import json
from app.app_config import AppConfig
from app.print_service import process_order

def kafka_consumer_loop(consumer):
    for message in consumer:
        try:
            print(f"Received order: {message.value}")
            order_data = message.value
            process_order(order_data)
        except Exception as e:
            print(f"Error in kafka_consumer_loop: {e}")

def start_kafka_consumer():
    consumer = KafkaConsumer(
        AppConfig.ORDER_TOPIC,
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
