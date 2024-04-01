import os

import requests
from dotenv import load_dotenv
from flask import Flask, Response, request

load_dotenv()

app = Flask(__name__)

PROPEL_TRY_AUTH_URL = os.getenv("PROPEL_TRY_AUTH_URL")
PROPEL_TRY_API_KEY = os.getenv("PROPEL_TRY_API_KEY")
TARGET_URL = "http://localhost:8501"  # The target URL you're proxying to


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(path):
    global TARGET_URL
    if request.method == "GET":
        resp = requests.get(f"{TARGET_URL}/{path}", params=request.args, headers=request.headers)
    elif request.method == "POST":
        resp = requests.post(f"{TARGET_URL}/{path}", json=request.json, headers=request.headers)
    elif request.method == "PUT":
        resp = requests.put(f"{TARGET_URL}/{path}", json=request.json, headers=request.headers)
    elif request.method == "DELETE":
        resp = requests.delete(f"{TARGET_URL}/{path}", headers=request.headers)
    elif request.method == "PATCH":
        resp = requests.patch(f"{TARGET_URL}/{path}", json=request.json, headers=request.headers)
    else:
        return "Unsupported HTTP method", 405

    excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
    headers = [
        (name, value)
        for (name, value) in resp.raw.headers.items()
        if name.lower() not in excluded_headers
    ]
    response = Response(resp.content, resp.status_code, headers)
    return response


if __name__ == "__main__":
    app.run(port=8000)
