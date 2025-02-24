from confluent_kafka.admin import AdminClient
from confluent_kafka import ConsumerGroupTopicPartitions, TopicPartition


class KafkaOffsetAdmin:
    def __init__(self, group_id: str, topic: str, bootstrap_servers: str):
        self.group_id = group_id
        self.topic = topic
        self.client = AdminClient({
            "bootstrap.servers": bootstrap_servers
        })

    def get_latest_offset(self):
        _partitions = ConsumerGroupTopicPartitions(group_id=self.group_id)
        _offsets = self.client.list_consumer_group_offsets([_partitions])
        offset = _offsets.get(self.group_id) if _offsets else None
        topic_partitions: list[TopicPartition] = offset.result().topic_partitions
        return sum(t.offset for t in topic_partitions)
