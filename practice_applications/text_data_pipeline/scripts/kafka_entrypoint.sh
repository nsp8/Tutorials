#!/bin/bash

# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."
#while ! nc -z kafka_broker 9092; do
sleep 30
#done

echo "Kafka is ready, creating topics..."

# Create topics
/opt/kafka/bin/kafka-topics.sh --create --topic youtube-videos --bootstrap-server localhost:9092 --partitions 2 --replication-factor 1

echo "Topics created successfully!"

exec "$@"
