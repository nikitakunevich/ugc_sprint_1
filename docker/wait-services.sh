#!/bin/sh

cmd="$@"

while ! nc -z -v 'kafka-1' 9092;
do
  >&2 echo "Kafka is unavailable - sleeping"
  sleep 2;
done

exec $cmd
