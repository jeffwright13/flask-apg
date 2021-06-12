import logging
import os
from pathlib import Path

from flask import render_template, request
import requests

from app import app
from .utils import upload_to_s3

AWS_GATEWAY_URL = os.getenv("AWS_GATEWAY_URL")


@app.route("/setvals", methods=("GET", "POST"))
def setvals():
    # All requests other than POST (i.e. GET) are re-shown the input form.
    if not request.method == "POST":
        return render_template("public/setvals2.html")

    # Local handles for request object (type: Werkzeug FileStorage)
    req_phrase_file_obj = request.files["phrase_file"]
    req_sound_file_obj = request.files["sound_file"]

    # Verify phrase_file type is allowed; if not, redirect to input form.
    if (
        Path(req_phrase_file_obj.filename).suffix
        not in app.config["PHRASEFILE_EXTENSIONS"]
    ):
        return render_template("public/setvals.html")

    # Checkbox takes value "on" if enabled; null otherwise
    to_mix = True if request.form.get("to_mix") == "on" else False

    # Set rest of parameters if 'mix' option was selected
    if to_mix:
        attenuation = request.form.get("attenuation")
        attenuation = int(attenuation) if attenuation else 0

        # Verify sound_file type is allowed; if not, redirect to input form.
        if (
            Path(req_sound_file_obj.filename).suffix
            not in app.config["SOUNDFILE_EXTENSIONS"]
        ):
            return render_template("public/setvals.html")

    # upload files to S3
    phrase_file_s3_path = upload_to_s3(req_phrase_file_obj)
    sound_file_s3_path = upload_to_s3(req_sound_file_obj)

    # have AWS lambda do the audio processing
    payload = dict(
        phrase_file=phrase_file_s3_path,
        sound_file=sound_file_s3_path,
        to_mix=to_mix,
        attenuation=attenuation)

    resp = requests.post(AWS_GATEWAY_URL, json=payload).json()

    response = resp["statusCode"]
    exception = resp.get("exception")
    # TODO: have the lambda function store the result file in the same or a
    # different S3 bucket, then check this cache here first for quick retrieval
    file = resp.get("result_file")

    if response == 200:
        logging.debug(
            f"AWS processed input files and generated file: {file}")
    else:
        logging.error(
            (f"AWS called with payload: {payload} => "
             f"response: {response} / exception: {exception}"))

    return render_template("public/setvals.html",
                           file=file,
                           exception=exception)


def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@app.route("/shutdown", methods=["GET"])
def shutdown():
    shutdown_server()
    return "Server shutting down..."
