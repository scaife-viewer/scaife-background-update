import base64
import datetime
import json

import google.auth
from google.auth.transport.requests import AuthorizedSession


def update_corpus(message, context):
    if "data" in message:
        decoded = base64.b64decode(message["data"]).decode("utf-8")
        payload = json.loads(decoded)
    else:
        payload = {}

    credentials, project_id = google.auth.default()
    http = AuthorizedSession(credentials)

    create_build(http, project_id)


def create_build(http, project_id):
    tag = datetime.datetime.now().strftime("%Y-%m-%d_%H")
    url = f"https://cloudbuild.googleapis.com/v1/projects/{project_id}/builds"
    headers = {
        "Content-Type": "application/json",
    }
    build = {
        "source": {
            "repoSource": {
                "repoName": "github-scaife-viewer-scaife-cts-api",
                "branchName": "master",
            },
        },
        "steps": [
            {
                "name": "gcr.io/cloud-builders/docker",
                "args": [
                    "build",
                    f"--tag=gcr.io/scaife-viewer/scaife-cts-api:{tag}",
                    ".",
                ],
            }
        ],
        "images": [
            f"gcr.io/scaife-viewer/scaife-cts-api:{tag}"
        ],
    }
    res = http.post(url, data=json.dumps(build), headers=headers)
    res.raise_for_status()
