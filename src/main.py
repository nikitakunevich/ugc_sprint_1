import logging
from typing import Optional

from confluent_kafka.cimpl import KafkaException
from fastapi import FastAPI

from kafka import AIOProducer, create_topics
from models import Event

logger = logging.getLogger(__name__)

app = FastAPI()
producer: Optional[AIOProducer] = None


@app.on_event("startup")
def startup_event():
    global producer
    producer = AIOProducer()

    create_topics()


@app.on_event("shutdown")
def shutdown_event():
    producer.close()


@app.post("/collect", description="Сохраняет аналитические запросы", status_code=204)
async def create_item(event: Event):
    try:
        await producer.produce("events", event.dict())
    except KafkaException as exc:
        logger.exception(exc)
    return {}
