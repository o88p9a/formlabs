import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    SHIPPING_TOPIC = os.getenv('SHIPPING_TOPIC', 'printed_parts')

config = Config()
