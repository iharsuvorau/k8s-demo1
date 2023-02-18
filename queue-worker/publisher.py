import json
import time
import pika

host = "rabbitmq-service"
port = 5672
queue = "requests"

credentials = pika.PlainCredentials("guest", "guest")
parameters = pika.ConnectionParameters(
    host=host,
    port=port,
    credentials=credentials,
)

channel = None


def on_connected(connection):
    connection.channel(on_open_callback=on_channel_open)


def on_channel_open(new_channel):
    global channel, queue

    channel = new_channel
    channel.queue_declare(
        queue=queue,
        durable=False,
        exclusive=False,
        auto_delete=False,
        callback=on_queue_declared,
    )


def on_queue_declared(frame):
    global channel, queue

    print("Queue declared")

    while True:
        publish_message()
        time.sleep(5)


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
connection = pika.SelectConnection(parameters, on_open_callback=on_connected)

try:
    connection.ioloop.start()
except KeyboardInterrupt:
    connection.close()
    connection.ioloop.start()
