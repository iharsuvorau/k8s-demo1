# Automated Simod Queue

Create a kind cluster with the following configuration:

```shell
kind create cluster --config kind-cluster.yaml
```

On the host machine, the `/tmp/simod-volume` folder should exist and contain the `resources` folder from the Simod repository. Those resources have sample configuration and event logs that will be copied by the publisher to simulate a new user request.

Build docker images and push them to Docker Hub and the kind cluster:

```shell
ruby build_push_images.rb
```

Observe the logs of the worker:

```shell
kubectl logs deployment/wq-work -f
```