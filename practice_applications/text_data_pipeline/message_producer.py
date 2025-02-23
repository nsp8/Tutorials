from confluent_kafka import SerializingProducer, KafkaException


def on_delivery(err, record):
    if err:
        print(f"Encountered error: {err}")
    else:
        print(f"Message delivered to: {record.topic()} [{record.partition()}]")


class KafkaProducer:
    def __init__(self, bootstrap_servers: str):
        self.producer_config = {
            "bootstrap.servers": bootstrap_servers,
        }
        self.producer = None

    def __enter__(self):
        self.producer = SerializingProducer(self.producer_config)
        return self

    def produce_message(self, topic, key, value):
        try:
            self.producer.produce(
                topic=topic,
                key=key,
                value=value,
                on_delivery=on_delivery
            )
        except KafkaException as ke:
            print(f"Encountered KafkaException: {ke}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.producer:
            self.producer.flush()
        if exc_type:
            print(f"Exception occurred: {exc_val}")
