import json
import logging
from requests_sse import EventSource


def invoke_firehose_api():
    logging.info("Starting ...")
    with EventSource(
        "http://github-firehose.libraries.io/events",
        timeout=30
    ) as event_source:
        for event in event_source:
            data = json.loads(event.data)
            logging.info(f"Got {data}")


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    try:
        invoke_firehose_api()
    except KeyboardInterrupt:
        logging.info("Exited.")
