# Specify BROKER_URL and QUEUE when running
FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y ca-certificates amqp-tools \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ADD populate_queue.sh /populate_queue.sh

CMD  bash /populate_queue.sh