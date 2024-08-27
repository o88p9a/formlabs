from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaProducer
from .config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    with app.app_context():
        db.create_all()

    return app

def create_kafka_producer(app):
    producer = KafkaProducer(
        bootstrap_servers=app.config['KAFKA_BOOTSTRAP_SERVERS'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    return producer
