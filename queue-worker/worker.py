from kubernetes import client, config
import pika


host = "rabbitmq-service"
port = 5672
queue = "requests"

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
    channel.basic_consume(queue=queue, on_message_callback=on_message)


def on_message(channel, method_frame, header_frame, body):
    print(
        "Received message # {} from {}: {}".format(
            method_frame.delivery_tag, header_frame.app_id, body
        )
    )
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def print_api_versions():
    config.load_incluster_config()

    print("Supported APIs (* is preferred version):")
    print("%-40s %s" % ("core", ",".join(client.CoreApi().get_api_versions().versions)))
    for api in client.ApisApi().get_api_versions().groups:
        versions = []
        for v in api.versions:
            name = ""
            if v.version == api.preferred_version.version and len(api.versions) > 1:
                name += "*"
            name += v.version
            versions.append(name)
        print("%-40s %s" % (api.name, ",".join(versions)))


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
