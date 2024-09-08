from fastapi import FastAPI
from app.database import SessionLocal, init_database
from typing import AsyncIterator

from app.kafka import start_kafka_consumer, stop_kafka_consumer
from app.print_service import start_batch_processor
from app.routes import router

# Lifespan event handler
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup tasks
    print("Starting up")
    app.state.consumer, app.state.consumer_thread = start_kafka_consumer()
    start_batch_processor()
    try:
        yield
    finally:
        print("Shutting down")
        stop_kafka_consumer(app.state.consumer, app.state.consumer_thread)

app = FastAPI(lifespan=lifespan)

init_database()

app.include_router(router, prefix="/api")
