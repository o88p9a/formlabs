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

def print_sample_parts(batch):
    """
    Simulates printing a batch of sample parts.
    """
    logger.info(f"Starting to print batch: {batch}")
    try:
        # Simulate printing each item in the batch
        for item in batch['items']:
            logger.info(f"Printing {item['quantity']} of sample part {item['sample_part_id']} with material {item['material_id']}")
            time.sleep(2)  # Simulate printing time
            logger.info(f"Finished printing {item['quantity']} of sample part {item['sample_part_id']}")
    except Exception as e:
        logger.error(f"Error while printing batch: {str(e)}")

def process_order(order):
    """
    Processes an order by grouping items into batches and printing them.
    """
    logger.info(f"Processing order: {order}")

    # Group items by sample part and material
    batches = {}
    for item in order.get('items', []):
        key = (item['sample_part_id'], item['material_id'])
        if key not in batches:
            batches[key] = {'sample_part_id': item['sample_part_id'], 'material_id': item['material_id'], 'items': []}
        batches[key]['items'].append(item)

    # Print each batch
    for batch in batches.values():
        print_sample_parts(batch)

def main():
    consumer = setup_kafka_consumer()
    producer = setup_kafka_producer()

    for message in consumer:
        order = message.value
        logger.info(f"Received order: {order}")

        try:
            process_order(order)
            # After printing, produce a message to another topic if needed
            producer.send('printed_parts', value={'order_id': order['id'], 'status': 'printed'})
            producer.flush()
        except Exception as e:
            logger.error(f"Error processing order: {str(e)}")

if __name__ == "__main__":
    main()
