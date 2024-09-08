import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class AppConfig:
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', '127.0.0.1:9092')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///orders.db')
