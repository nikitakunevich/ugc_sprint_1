#!/bin/sh

cmd="$@"

while ! nc -z -v 'kafka-1' 9092;
do
  >&2 echo "Kafka is unavailable - sleeping"
  sleep 2;
done

while ! nc -z -v 'clickhouse-node1' 9000;
do
  >&2 echo "Clickhouse is unavailable - sleeping"
  sleep 2;
done

exec $cmd