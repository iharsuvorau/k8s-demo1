import json
import os
import time
import pika


def publish_message():
    global channel, queue

    message = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}

    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            app_id="publisher.py",
            content_type="application/json",
        ),
    )

    print("Sent message # {}".format(message))


broker_url = os.environ.get("BROKER_URL")
queue = os.environ.get("REQUESTS_QUEUE", "requests")

parameters = pika.URLParameters(broker_url)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

while True:
    try:
        publish_message()
    except:
        print("Failed to publish message")

    time.sleep(5)
