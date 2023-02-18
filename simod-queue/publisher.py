import json
import os
from pathlib import Path
import shutil
import time
import traceback
import uuid
import pika

base_dir = Path("/tmp/simod-volume")


def create_request_folder() -> str:
    global base_dir

    request_id = str(uuid.uuid4())
    request_dir = base_dir / request_id
    request_dir.mkdir(parents=True, exist_ok=True)

    config_path = base_dir / "resources/config/sample.yml"
    request_config_path = request_dir / "config.yaml"
    shutil.copy(config_path, request_config_path)

    with request_config_path.open("r+") as f:
        config = f.read()
        config = config.replace(
            "data/resources/event_logs/PurchasingExample.xes",
            f"data/{request_id}/event_log.xes",
        )
        f.write(config)

    event_log_path = base_dir / "resources/event_logs/PurchasingExample.xes"
    shutil.copy(event_log_path, request_dir / "event_log.xes")

    return request_id


def publish_message():
    global channel, queue

    message = create_request_folder()

    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=message,
        properties=pika.BasicProperties(
            app_id="publisher.py",
            content_type="text/plain",
        ),
    )

    print(f"Sent message: {message}")


broker_url = os.environ.get("BROKER_URL")
queue = os.environ.get("REQUESTS_QUEUE", "requests")

parameters = pika.URLParameters(broker_url)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

while True:
    try:
        publish_message()
    except Exception as e:
        print(f"Failed to publish message. Error: {e}")
        traceback.print_exc()

    time.sleep(15)
