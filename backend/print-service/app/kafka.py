import threading
from kafka import KafkaConsumer, KafkaProducer
import json
from app.database import SessionLocal
from app.models import PrintOrder, PrintOrderItem
from app.app_config import AppConfig

def process_order(order_data):
    db = SessionLocal()
    try:
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
    except Exception as e:
        print(f"Error processing order: {e}")
        db.rollback()
    finally:
        db.close()

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
        "order",
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
