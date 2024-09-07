import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    PRINT_TOPIC = os.getenv('PRINT_TOPIC', 'orders')

config = Config()
