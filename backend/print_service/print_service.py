import json
import logging
import time
from kafka import KafkaConsumer, KafkaProducer
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_kafka_consumer():
    try:
        consumer = KafkaConsumer(
            config.PRINT_TOPIC,
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='print-service-group'
        )
        logger.info(f"Kafka Consumer connected to {config.KAFKA_BOOTSTRAP_SERVERS} on topic {config.PRINT_TOPIC}")
        return consumer
    except Exception as e:
        logger.error(f"Failed to set up Kafka consumer: {str(e)}")
        raise

def setup_kafka_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        logger.info(f"Kafka Producer connected to {config.KAFKA_BOOTSTRAP_SERVERS}")
        return producer
    except Exception as e:
        logger.error(f"Failed to set up Kafka producer: {str(e)}")
        raise

def print_sample_part(order_item):
    logger.info(f"Starting to print {order_item['quantity']} of sample part {order_item['sample_part_id']} with material {order_item['material_id']}")
    try:
        # Simulate the printing process
        time.sleep(2)
        logger.info(f"Finished printing {order_item['quantity']} of sample part {order_item['sample_part_id']}")
    except Exception as e:
        logger.error(f"Error while printing: {str(e)}")

def main():
    consumer = setup_kafka_consumer()
    producer = setup_kafka_producer()

    for message in consumer:
        order = message.value
        logger.info(f"Received order: {order}")

        for item in order.get('items', []):
            print_sample_part(item)
        
        # After printing, produce a message to another topic if needed
        producer.send('printed_parts', value={'order_id': order['id'], 'status': 'printed'})
        producer.flush()

if __name__ == "__main__":
    main()
