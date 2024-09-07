from fastapi import FastAPI
from app.database import SessionLocal, init_database
from app.app_config import AppConfig
from kafka import KafkaProducer
import json
from typing import AsyncIterator
from app.routes import router


# Kafka Producer Dependency
def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=AppConfig.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

# Lifespan event handler
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup tasks
    print("Starting up  " + AppConfig.KAFKA_BOOTSTRAP_SERVERS)
    app.state.db = SessionLocal()
    app.state.kafka_producer = get_kafka_producer()

    yield  # Control is handed to the application for processing

    # Shutdown tasks
    print("Shutting down")
    app.state.db.close()
    app.state.kafka_producer.close()

# Initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

init_database()

app.include_router(router, prefix="/api")
