import asyncio
import json
import logging
from asyncio import Future
from threading import Thread

from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.cimpl import KafkaException, Message

from config import settings

logger = logging.getLogger(__name__)


class AIOProducer:
    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self._producer = Producer({"bootstrap.servers": settings.kafka_hosts_as_string})
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)

    def start(self) -> None:
        self._poll_thread.start()

    def _poll_loop(self) -> None:
        while not self._cancelled:
            self._producer.poll(0.1)

    def close(self) -> None:
        self._cancelled = True
        self._poll_thread.join()

    def produce(self, topic: str, message: dict) -> "Future[Message]":
        """ Создает сообщение для Kafka и возвращает Future объект. """
        result = self._loop.create_future()

        def ack(err, msg):
            if err:
                self._loop.call_soon_threadsafe(
                    result.set_exception, KafkaException(err)
                )
            else:
                self._loop.call_soon_threadsafe(result.set_result, msg)

        message = json.dumps(message).encode()
        self._producer.produce(topic, message, on_delivery=ack)
        return result


def create_topics() -> None:
    """ Создает топики, указанные в настройках."""
    admin_client = AdminClient({"bootstrap.servers": settings.kafka_hosts_as_string})

    new_topics = [
        NewTopic(topic, num_partitions=3, replication_factor=1)
        for topic in settings.kafka_topics
    ]

    futures = admin_client.create_topics(new_topics)

    for topic, future in futures.items():
        try:
            future.result()
            logger.info(f"Топик {topic} был создан.")
        except Exception as e:
            logger.error(f"Ошибка при создании топика {topic}: {repr(e)}")
