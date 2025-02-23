import json
import logging
import os
import sys
import time
from pprint import pformat
from dotenv import load_dotenv
import requests
import constants
from message_producer import KafkaProducer

load_dotenv()


def summarize_data(video_object: dict) -> dict:
    return {
        "video_id": video_object.get("id"),
        "title": video_object.get("snippet").get("title"),
        "published_at": video_object.get("snippet").get("publishedAt"),
        "likes": int(video_object.get("statistics").get("likeCount", 0)),
        "views": int(video_object.get("statistics").get("viewCount", 0)),
        "comments": int(video_object.get("statistics").get("commentCount", 0)),
    }


def fetch_playlist_items_page(
    api_key: str, playlist_id: str, page_token: str | None = None
):
    paged_response = requests.get(constants.YOUTUBE_API_PLAYLIST_URL, params={
        "key": api_key,
        "playlistId": playlist_id,
        "part": "contentDetails",
        "pageToken": page_token,
    })
    payload = json.loads(paged_response.text)
    if paged_response.status_code not in (200, 300):
        logging.info(pformat(paged_response.json()))
    return payload


def fetch_videos_page(api_key: str, video_id: str):
    paged_response = requests.get(constants.YOUTUBE_API_VIDEO_URL, params={
        "key": api_key,
        "id": video_id,
        "part": "snippet,statistics",
    })
    # if paged_response.status_code not in (200, 300):
    # logging.info(pformat(paged_response.json()))
    payload = json.loads(paged_response.text)
    return payload


def fetch_playlist_items(
    api_key: str, playlist_id: str, page_token: str | None = None
):
    payload = fetch_playlist_items_page(api_key, playlist_id, page_token)
    yield from payload.get("items")
    next_page_token = payload.get("nextPageToken")
    if next_page_token:
        yield from fetch_playlist_items(api_key, playlist_id, next_page_token)


def fetch_videos(api_key: str, video_id: str):
    payload = fetch_videos_page(api_key, video_id)
    yield from payload.get("items")


def show_collection(playlist_videos: list) -> None:
    logging.info(pformat(playlist_videos))


def collect_youtube_playlist(stream: bool = False) -> None:
    logging.info("START")
    api_key = os.getenv("YOUTUBE_API_KEY")
    playlist_id = constants.PLAYLIST_ID
    videos: list = list()
    if not stream:
        logging.info("Collecting data ...")
    for item in fetch_playlist_items(api_key, playlist_id):
        video_id = item.get("contentDetails").get("videoId")
        for video in fetch_videos(api_key, video_id):
            video_data = summarize_data(video)
            if video_data not in videos:
                if stream:
                    logging.info(pformat(video_data))

                videos.append(video_data)
                with KafkaProducer(
                    bootstrap_servers=constants.BOOTSTRAP_SERVERS
                ) as producer:
                    producer.produce_message(
                        topic=constants.KAFKA_TOPIC,
                        key=video_id,
                        value=json.dumps(video_data)
                    )
        time.sleep(2)
    show_collection(videos)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        sys.exit(collect_youtube_playlist())
    except KeyboardInterrupt:
        logging.info("Exiting ...")
