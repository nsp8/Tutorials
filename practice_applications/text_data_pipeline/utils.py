import json
from pprint import pformat
import requests
from practice_applications.text_data_pipeline import constants


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
) -> dict:
    paged_response = requests.get(constants.YOUTUBE_API_PLAYLIST_URL, params={
        "key": api_key,
        "playlistId": playlist_id,
        "part": "contentDetails",
        "pageToken": page_token,
    })
    payload = json.loads(paged_response.text)
    if paged_response.status_code not in (200, 300):
        print(pformat(paged_response.json()))
    return payload


def fetch_videos_page(api_key: str, video_id: str) -> dict:
    paged_response = requests.get(constants.YOUTUBE_API_VIDEO_URL, params={
        "key": api_key,
        "id": video_id,
        "part": "snippet,statistics",
    })
    # if paged_response.status_code not in (200, 300):
    # print(pformat(paged_response.json()))
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
    print(pformat(playlist_videos))
