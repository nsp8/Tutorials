
import json
import logging
import os
import queue
import sys
import threading
import time
from pprint import pformat
from dotenv import load_dotenv
from confluent_kafka import Consumer, KafkaError, KafkaException
from practice_applications.text_data_pipeline import constants
from practice_applications.text_data_pipeline.database import write_to_database
from practice_applications.text_data_pipeline.kafka_admin import KafkaOffsetAdmin
from practice_applications.text_data_pipeline.message_producer import KafkaProducer
from practice_applications.text_data_pipeline import utils

load_dotenv()
queue = queue.Queue()
admin = KafkaOffsetAdmin(
    group_id=constants.GROUP_ID,
    topic=constants.KAFKA_TOPIC,
    bootstrap_servers=constants.BOOTSTRAP_SERVERS
)


def collect_youtube_playlist(stream: bool = False) -> None:
    logging.info("START")
    api_key = os.getenv("YOUTUBE_API_KEY")
    playlist_id = constants.PLAYLIST_ID
    videos: list = list()
    if not stream:
        logging.info("Collecting data ...")
    with KafkaProducer(
            bootstrap_servers=constants.BOOTSTRAP_SERVERS
    ) as producer:
        for item in utils.fetch_playlist_items(api_key, playlist_id):
            video_id = item.get("contentDetails").get("videoId")
            for video in utils.fetch_videos(api_key, video_id):
                video_data = utils.summarize_data(video)
                if video_data not in videos:
                    if stream:
                        logging.info(pformat(video_data))
                    # produce messages
                    video_data["playlist_id"] = playlist_id
                    producer.produce_message(
                        topic=constants.KAFKA_TOPIC,
                        key=video_id,
                        value=json.dumps(video_data)
                    )

                    # get latest offset and set it in the queue
                    latest_offset = admin.get_latest_offset()
                    logging.debug(f"\t<<< Writing {latest_offset=}")
                    queue.put(latest_offset)
                    videos.append(video_data)
            time.sleep(2)
    utils.show_collection(videos)


def consume_messages():
    consumer_config: dict = {
        "bootstrap.servers": constants.BOOTSTRAP_SERVERS,
        "group.id": constants.GROUP_ID,
        "auto.offset.reset": "earliest",
    }
    consumer = Consumer(consumer_config)
    consumer.subscribe(topics=[constants.KAFKA_TOPIC])
    try:
        while True:
            # consume messages from the stream
            message = consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(message.error())
            # read the latest offset from the queue
            latest_offset = queue.get()
            logging.debug(f"\t>>> Reading {latest_offset=}")
            data_received = json.loads(message.value().decode("utf-8"))
            logging.info(f"Consumed: {pformat(data_received)}")

            # writing to the database
            write_to_database(data_received)
    except KeyboardInterrupt:
        logging.info("Stopping consumer ...")
    finally:
        consumer.close()


def main():
    producer_thread = threading.Thread(target=collect_youtube_playlist)
    consumer_thread = threading.Thread(target=consume_messages, daemon=True)
    producer_thread.start()
    consumer_thread.start()
    producer_thread.join()
    consumer_thread.join()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logging.info("Exiting ...")
