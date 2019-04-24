# Flask
from flask import Flask, render_template
import requests
import os, random

# Datadog tracing and metrics
from datadog import initialize, statsd
from ddtrace import tracer, patch_all
if "DOGSTATSD_HOST_IP" in os.environ:
  initialize(statsd_host = os.environ.get("DOGSTATSD_HOST_IP"))
  tracer.configure(hostname = os.environ.get("DOGSTATSD_HOST_IP"))
patch_all()

app = Flask(__name__)
env = os.environ.get("DD_SERVICE_ENV")
conf = os.environ.get("DD_CONF_NAME")
tags = ["env:" + env, "conference:" + conf]

@app.route("/")
def index():
  statsd.increment("dat_a_dog.pageviews", tags = tags + ["page:index"])
  return render_template("dat-a-dog.html", image = get_image(), conference = conf)

@app.route("/is-dog/<is_dog>")
def count_dog(is_dog):
  # Count page views.
  statsd.increment("dat_a_dog.pageviews", tags = tags + ["page:count_dog"])

  if is_dog == "yes":
    statsd.increment("dat_a_dog.counted.dogs", tags = tags)
    message = "Such woof! Very dog! MOAR?"
  else:
    statsd.increment("dat_a_dog.counted.not_dogs", tags = tags)
    message = "Not doge. I can haz another?"

  return render_template("dat-a-dog.html", image = get_image(), conference = conf, message = message)


def get_image():
  if random.randint(0,1):
    statsd.increment("dat_a_dog.generated.dogs", tags = tags)
    r = requests.get("https://dog.ceo/api/breeds/image/random")
    data = r.json()
    return data["message"]
  else:
    statsd.increment("dat_a_dog.generated.not_dogs", tags = tags)
    r = requests.get("https://api.thecatapi.com/v1/images/search")
    data = r.json()
    return data[0]["url"]


if __name__ == "__main__":
    app.run(host = "0.0.0.0")
