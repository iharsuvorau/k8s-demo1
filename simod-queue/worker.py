import os
from kubernetes import client, config
import pika


def on_message(channel, method_frame, header_frame, body):
    print(
        "Received message # {} from {}: {}".format(
            method_frame.delivery_tag, header_frame.app_id, body
        )
    )

    process_request(body)

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def process_request(message):
    message = str(message, "utf-8")

    print("Processing request: {}".format(message))

    config_path = f"/usr/src/Simod/data/{message}/config.yaml"
    output_dir = f"/usr/src/Simod/data/{message}"

    config.load_incluster_config()

    with client.ApiClient() as api_client:
        api_instance = client.BatchV1Api(api_client)
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=f"simod-{message}"),
            spec=client.V1JobSpec(
                ttl_seconds_after_finished=5,
                template=client.V1PodTemplateSpec(
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name="simod",
                                image="nokal/simod:v3.2.1",
                                command=[
                                    "bash",
                                    "run.sh",
                                    config_path,
                                    output_dir,
                                ],
                                resources=client.V1ResourceRequirements(
                                    requests={"cpu": "100m", "memory": "128Mi"},
                                    limits={"cpu": "1", "memory": "1Gi"},
                                ),
                                volume_mounts=[
                                    client.V1VolumeMount(
                                        name="simod-data",
                                        mount_path="/usr/src/Simod/data",
                                    ),
                                ],
                            )
                        ],
                        restart_policy="Never",
                        volumes=[
                            client.V1Volume(
                                name="simod-data",
                                persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                    claim_name="simod-volume-claim"
                                ),
                            )
                        ],
                    )
                ),
            ),
        )

        try:
            api_instance.create_namespaced_job(namespace="default", body=job)
        except client.rest.ApiException as e:
            print(
                "Exception when calling BatchV1Api->create_namespaced_job: %s, %s"
                % (e, e.body)
            )


broker_url = os.environ.get("BROKER_URL")
requests_queue = os.environ.get("REQUESTS_QUEUE", "requests")

parameters = pika.URLParameters(broker_url)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.basic_consume(queue=requests_queue, on_message_callback=on_message)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()

print("Done")
