import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class AppConfig:
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', '127.0.0.1:9092')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///print.db')
    ORDER_TOPIC = os.getenv('ORDER_TOPIC', 'order')
    ORDER_PRINTED_TOPIC = os.getenv('PRINT_TOPIC', 'order_printed')

