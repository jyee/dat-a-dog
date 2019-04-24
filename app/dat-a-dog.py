# Flask
from flask import Flask, render_template
import requests
import os, random

# Datadog tracing and metrics
from datadog import initialize, statsd
from ddtrace import tracer, patch_all

# If we're getting a DogStatD host (i.e. running in Kubernetes), initialize with it.
if "DOGSTATSD_HOST_IP" in os.environ:
  initialize(statsd_host = os.environ.get("DOGSTATSD_HOST_IP"))
  tracer.configure(hostname = os.environ.get("DOGSTATSD_HOST_IP"))

# Apply some base tags and patch for Datadog tracing.
statsd.constant_tags = ["env:confdemo"]
patch_all()

app = Flask(__name__)


@app.route("/")
def index():
  statsd.increment("dat_a_dog.pageviews", tags = ["page:index"])
  return render_template("dat-a-dog.html", image = get_image(), conference = os.environ.get("DD_CONF_NAME"))


@app.route("/is-dog/<is_dog>")
def count_dog(is_dog):
  statsd.increment("dat_a_dog.pageviews", tags = ["page:count_dog"])

  if is_dog == "yes":
    statsd.increment("dat_a_dog.counted.dogs")
    message = "Such woof! Very dog! MOAR?"
  else:
    statsd.increment("dat_a_dog.counted.not_dogs")
    message = "Not doge. I can haz another?"

  return render_template("dat-a-dog.html", image = get_image(), conference = os.environ.get("DD_CONF_NAME"), message = message)


def get_image():
  # Randomize between our dog and cat sources. Each API returns an image URL.
  if random.randint(0,1):
    statsd.increment("dat_a_dog.generated.dogs")
    r = requests.get("https://dog.ceo/api/breeds/image/random")
    data = r.json()
    return data["message"]
  else:
    statsd.increment("dat_a_dog.generated.not_dogs")
    r = requests.get("https://api.thecatapi.com/v1/images/search")
    data = r.json()
    return data[0]["url"]


if __name__ == "__main__":
    app.run(host = "0.0.0.0")
