import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class AppConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', '127.0.0.1:9092')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///orders.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

