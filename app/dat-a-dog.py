# Flask
from flask import Flask, render_template
import requests
import os, random

# Datadog tracing and metrics
from datadog import statsd
from ddtrace import patch_all
patch_all()

app = Flask(__name__)
env = os.environ.get("DD_SERVICE_ENV")
conf = os.environ.get("DD_CONF_NAME")

@app.route("/")
def index():
  tags = ["env:" + env, "conference:" + conf, "page:index"]
  return render_template("dat-a-dog.html", image = get_image(), conference = conf)

@app.route("/is-dog/<is_dog>")
def count_dog(is_dog):
  # Count page views.
  tags = ["env:" + env, "conference:" + conf, "page:count_dog"]
  statsd.increment("dat-a-dog.pageviews", tags = tags)

  if is_dog == "yes":
    statsd.increment("dat-a-dog.dogs", tags = tags)
    message = "Such woof! Very dog! MOAR?"
  else:
    statsd.increment("dat-a-dog.not-dogs", tags = tags)
    message = "Not doge. I can haz another?"

  return render_template("dat-a-dog.html", image = get_image(), conference = conf, message = message)


def get_image():
  if random.randint(0,1):
    r = requests.get("https://dog.ceo/api/breeds/image/random")
    data = r.json()
    return data["message"]
  else:
    r = requests.get("https://api.thecatapi.com/v1/images/search")
    data = r.json()
    return data[0]["url"]


if __name__ == "__main__":
    app.run()
