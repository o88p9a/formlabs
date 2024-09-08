from fastapi import FastAPI
from app.database import SessionLocal, init_database
from app.app_config import AppConfig
from kafka import KafkaProducer
import json
from typing import AsyncIterator
from app.routes import router

def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=AppConfig.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("Starting up")
    app.state.db = SessionLocal()
    app.state.kafka_producer = get_kafka_producer()

    yield 

    print("Shutting down")
    app.state.db.close()
    app.state.kafka_producer.close()

app = FastAPI(lifespan=lifespan)

init_database()

app.include_router(router, prefix="/api")
