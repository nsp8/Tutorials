import json
import requests
from quixstreams import Application

app = Application(
    broker_address="localhost:9092",
    loglevel="DEBUG"
)


def fetch_temperature(latitude: float, longitude: float) -> dict | None:
    """Fetches current temperature 2m above sea level"""
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m",
        }
    )
    if response.status_code in range(200, 300):
        return response.json()
    return None


def create_producer(key: str, data: dict) -> None:
    with app.get_producer() as producer:
        producer.produce(
            topic="weather_data",
            key=key,
            value=json.dumps(data)
        )


if __name__ == "__main__":
    # Toronto weather
    temperature_data = fetch_temperature(
        latitude=43.6532,
        longitude=79.3832
    )
    if temperature_data:
        create_producer(key="toronto_temperature", data=temperature_data)
