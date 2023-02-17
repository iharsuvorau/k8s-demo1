# Simod Job with a Shared Persistent Volume

Create a folder at `/tmp/simod-volume` on the host machine and copy `resources` folder from the Simod repository into it.

```bash
mkdir /tmp/simod-volume
cp -r /path/to/simod/resources /tmp/simod-volume
```

Create a cluster:

```bash
kind create cluster --config kind-cluster.yaml
```

Load the Simod image into the cluster nodes:

```bash
kind load docker-image nokal/simod:v3.2.1
```

Run the deployment that contains a persisntent volume, persistent volume claim and a job:

```bash
kubectl apply -f deployment.yaml
```

It would start a Simod job on a sample configuration that we attached to nodes located at the `/tmp/simod-volume/resources` folder. The output is saved to `/tmp/simod-volume/outputs` folder.

Check the logs of the job:

```bash
kubectl logs -f simod-job
```
