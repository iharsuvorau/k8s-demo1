# Parallel Job Execution with RabbitMQ

Create a cluster with kind:

```shell
kind create cluster --config kind-cluster.yaml
```

Deploy RabbitMQ:

```shell
kubectl create -f https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.3/examples/celery-rabbitmq/rabbitmq-service.yaml

kubectl create -f https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.3/examples/celery-rabbitmq/rabbitmq-controller.yaml
```

Build and push the publisher Docker image:

```shell
docker build -t nokal/k8s-samples-wq-publisher:v1 -f publisher.dockerfile .
docker push nokal/k8s-samples-wq-publisher:v1
```

Build and push the worker Docker image:

```shell
docker build -t nokal/k8s-samples-wq-worker:v1 -f worker.dockerfile .
docker push nokal/k8s-samples-wq-worker:v1
```

Load the images into the kind cluster:

```shell
kind load docker-image nokal/k8s-samples-wq-worker:v1
kind load docker-image nokal/k8s-samples-wq-publisher:v1
```

Run the publisher first to populate the queue and the worker to consume the messages:

```shell
kubectl apply -f publisher.yaml
kubectl apply -f worker.yaml
```

Check the logs of the worker:

```shell
kubectl describe -f worker.yaml
```

At the end, there should be 8 successful job runs.