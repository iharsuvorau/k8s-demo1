import json
import time
import pika

host = "rabbitmq-service"
port = 5672
queue = "requests"
channel = None


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


credentials = pika.PlainCredentials("guest", "guest")
parameters = pika.ConnectionParameters(
    host=host,
    port=port,
    credentials=credentials,
)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

while True:
    try:
        publish_message()
    except:
        print("Failed to publish message")

    time.sleep(5)
