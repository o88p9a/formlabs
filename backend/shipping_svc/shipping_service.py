import json
import logging
import time
from kafka import KafkaConsumer
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_kafka_consumer():
    try:
        consumer = KafkaConsumer(
            config.SHIPPING_TOPIC,
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='shipping-service-group'
        )
        logger.info(f"Kafka Consumer connected to {config.KAFKA_BOOTSTRAP_SERVERS} on topic {config.SHIPPING_TOPIC}")
        return consumer
    except Exception as e:
        logger.error(f"Failed to set up Kafka consumer: {str(e)}")
        raise

def ship_sample_part(order):
    logger.info(f"Starting to ship order {order['id']} to customer {order['customer_id']}")
    try:
        # Simulate the shipping process
        time.sleep(2)
        logger.info(f"Finished shipping order {order['id']} to customer {order['customer_id']}")
    except Exception as e:
        logger.error(f"Error while shipping order {order['id']}: {str(e)}")

def main():
    consumer = setup_kafka_consumer()

    for message in consumer:
        order = message.value
        logger.info(f"Received order for shipping: {order}")
        ship_sample_part(order)

if __name__ == "__main__":
    main()
