# Kubernetes Demo Deployment

This is a demo app for exploring how Kubernetes works and scales.

For creating a cluster, I use [kind](https://kind.sigs.k8s.io/) v0.17.0.

Kubernetes versions:

```
Client Version: v1.25.4
Kustomize Version: v4.5.7
Server Version: v1.25.3
```

## Kind Cluster

Creating a local cluster with kind:

```shell
kind create cluster --config kind-cluster.yaml
```

Load the image into the cluster:

```shell
kind load docker-image k8s-demo1:v1
```


## Kubernetes Deployment with Imperative Commands

Creating a deployment:

```shell
kubectl create deployment demo1 --image=k8s-demo1:v1 --port=8080
```

It's important to not use the Docker tag `latest` for the image, because `kind` doesn't pull such images and `kubernetes` responds with `ErrImagePull` error.

Scaling the deployment:

```shell
kubectl scale --replicas=3 deployment/demo1
```

To access it, expose the ports:

```shell
kubectl port-forward deployment/demo1 :8080
```

In this way, `kubernetes` will find a free port on the host and forward it to the container port 8080. So, you can access the app at http://localhost:xxxxx where `xxxxx` is the port number printed by the command.

## Kubernetes Dashboard Addon (optional)

Install the dashboard:

```shell
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
helm install dashboard kubernetes-dashboard/kubernetes-dashboard -n kubernetes-dashboard --create-namespace
```

For dashboard access, run:

```shell
kubectl proxy
```

Create a token for admin-user for the dashboard:

```shell
kubectl create token admin-user -n kubernetes-dashboard
```

It would print out the token. Copy it and use it to login to the dashboard.

Access the dashboard at http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:dashboard-kubernetes-dashboard:https/proxy/#/login.


## Load Testing

```shell
ruby load_test.rb
```

However, I cannot confirm now that the load balancing works, because I get responses from the same container even though I have 3 replicas running.


## Load Balancing and Exposing The Service with Ingress

```shell
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

```shell
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

```shell
kubectl apply -f deployment.yaml
```

```shell
curl localhost:8080/demo1
```