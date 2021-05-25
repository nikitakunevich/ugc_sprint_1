#!/bin/sh

cmd="$@"

while ! nc -z -v $KAFKA_WAITER_HOST $KAFKA_WAITER_PORT;
do
  >&2 echo "Kafka is unavailable - sleeping"
  sleep 2;
done

exec $cmd