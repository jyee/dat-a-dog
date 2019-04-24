# Dat a dog?

This is just a silly example app to use for various demos.

## Running the app in Docker

You can use the Dockerfile in this repo to build it, or pull it directly from Docker Hub at [jyee/dat-a-dog](https://hub.docker.com/r/jyee/dat-a-dog).

Once you've built the container image or pulled it from Docker Hub, you can run it:

```
docker run -ti -p 5000:5000 -e DD_CONF_NAME="My Test Conf" dat-a-dog
```

The `DD_CONF_NAME` is use for the main greeting in the app header. It can be any string, but for the purposes of running demos at conferences and other events, it's best to use the conference name.

## Running the app in Kubernetes

To run this in Kubernetes, first edit the `dat-a-dog.yaml` file to update the `DD_CONF_NAME` environment variable. If you're using Minikube, you can apply the yaml file, then use minikube to launch the app in your default browser:

```
kubectl apply -f dat-a-dog.yaml
minikube service dat-a-dog
```
