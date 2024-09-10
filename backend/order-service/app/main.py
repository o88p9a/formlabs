from fastapi import FastAPI
from app.database import SessionLocal, init_database
from typing import AsyncIterator
from fastapi.middleware.cors import CORSMiddleware

from app.kafka import get_kafka_producer
from app.routes import router

async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("Starting up")
    app.state.db = SessionLocal()
    app.state.kafka_producer = get_kafka_producer()

    yield 

    print("Shutting down")
    app.state.db.close()
    app.state.kafka_producer.close()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust according to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_database()

app.include_router(router, prefix="/api")
