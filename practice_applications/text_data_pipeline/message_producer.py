from confluent_kafka import SerializingProducer, KafkaError
from constants import KAFKA_CONFIG, KAFKA_TOPIC


def on_delivery(err, record):
    ...


def produce_message(message: str) -> None:
    producer = SerializingProducer(KAFKA_CONFIG)
    try:
        pass
    except KafkaError as ke:
        print(f"Encountered KafkaError: {ke}")
    finally:
        producer.flush()
