from kubernetes import client, config
import pika


host = "rabbitmq-service"
port = 5672
queue = "requests"


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
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.basic_consume(queue=queue, on_message_callback=on_message)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()

print("Done")
