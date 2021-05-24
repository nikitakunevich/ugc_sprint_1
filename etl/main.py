import sys
import json
from confluent_kafka import Consumer, KafkaError, KafkaException
from clickhouse import init_clickhouse_database, save_to_clickhouse
from config import settings
from models import Event


# kafka client init
conf = {'bootstrap.servers': settings.kafka_hosts_as_string,
        'group.id': settings.kafka_consumer_group,
        'auto.offset.reset': 'smallest'}

consumer = Consumer(conf)
running = True


def consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while running:
            messages = consumer.consume(num_messages=100, timeout=1.0)
            if messages is None:
                continue

            for msg in messages:
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                         (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())

            parsed_messages = [Event(**json.loads(message.value())) for message in messages]
            save_to_clickhouse(parsed_messages)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def shutdown():
    global running
    running = False


if __name__ == '__main__':
    init_clickhouse_database()
    consume_loop(consumer, settings.kafka_topics)
