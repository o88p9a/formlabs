
from fastapi import FastAPI
from app.database import SessionLocal, init_database
from app.app_config import AppConfig
from typing import AsyncIterator

from app.kafka import start_kafka_consumer, stop_kafka_consumer
from app.routes import router

# Lifespan event handler
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup tasks
    print("Starting up")
    start_kafka_consumer()

    yield  

    print("Shutting down")
    stop_kafka_consumer()
app = FastAPI()

init_database()

app.include_router(router, prefix="/api")
