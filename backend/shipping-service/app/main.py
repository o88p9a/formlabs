from fastapi import FastAPI
from app.database import init_database
from typing import AsyncIterator

from app.kafka import start_kafka_consumer, stop_kafka_consumer

async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("Starting up")
    app.state.consumer, app.state.consumer_thread = start_kafka_consumer()
    try:
        yield
    finally:
        print("Shutting down")
        stop_kafka_consumer(app.state.consumer, app.state.consumer_thread)

app = FastAPI(lifespan=lifespan)

init_database()
