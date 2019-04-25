# Dat a dog?

This is just a silly example app to use for various demos.

<img src="https://github.com/jyee/dat-a-dog/raw/master/dat-a-dog.gif" alt="This app is useless if you're blind." style="width:50%; height:auto;" />

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

## Monitoring

The app is already instrumented to send metrics and traces to Datadog. If you need a basic dashboard, you can import the one in `datadog/dashboard.json`. To do this, you'll need your [Datadog API and APP keys](https://app.datadoghq.com/account/settings#api). Then run:

```
API_KEY="<YOUR API KEY>"
APP_KEY="<YOUR APP KEY>"
curl -X POST -H "Content-Type: application/json" -d "@datadog/dashboard.json"  "https://api.datadoghq.com/api/v1/dashboard?api_key=${API_KEY}&application_key=${APP_KEY}"
```

## Further resources

This app is used in the [Kubernetes HPA demo](https://github.com/jyee/k8s-hpa-demo).
