import os
from pathlib import Path

from flask import (
    render_template,
    request,
    redirect,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename
import requests

from app import app
from .utils import encode_mp3_file, upload_to_s3

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

    # Save the phrase file (if non-null) to local file-upload dir
    if req_phrase_file_obj.filename != "":
        req_phrase_file_obj.save(
            Path(app.config["FILE_FOLDER"])
            / Path(secure_filename(req_phrase_file_obj.filename))
        )
        req_phrase_file_obj.close()

    # Set fullpath local var to send to apg instance
    phrase_file = (
        Path(app.config["FILE_FOLDER"]) / Path(req_phrase_file_obj.filename)
        if req_phrase_file_obj.filename != ""
        else None
    )

    # Checkbox takes value "on" if enabled; null otherwise
    to_mix = True if request.form.get("to_mix") == "on" else False

    # Set rest of parameters if 'mix' option was selected
    if to_mix:
        attenuation = request.form.get("attenuation")
        attenuation = int(attenuation) if attenuation else 0

        # Set fullpath local var to send to apg instance
        sound_file = (
            Path(app.config["FILE_FOLDER"]) / Path(req_sound_file_obj.filename)
            if req_sound_file_obj.filename != ""
            else None
        )

        # Verify sound_file type is allowed; if not, redirect to input form.
        if (
            Path(req_sound_file_obj.filename).suffix
            not in app.config["SOUNDFILE_EXTENSIONS"]
        ):
            return render_template("public/setvals.html")

        # Save the sound file (if non-null) to local file-upload dir
        req_sound_file_obj = req_sound_file_obj
        if req_sound_file_obj.filename != "":
            req_sound_file_obj.save(
                Path(app.config["FILE_FOLDER"])
                / Path(secure_filename(req_sound_file_obj.filename))
            )
            req_sound_file_obj.close()

    # upload files to S3
    phrase_file_s3_path = upload_to_s3(phrase_file)
    sound_file_s3_path = upload_to_s3(sound_file)

    # have AWS lambda do the audio processing
    payload = dict(
        phrase_file=phrase_file_s3_path,
        sound_file=sound_file_s3_path,
        to_mix=to_mix,
        attenuation=attenuation)

    breakpoint()
    resp = requests.post(AWS_GATEWAY_URL, json=payload).json()
    encoded_result_mp3 = resp["result_file"]

    return render_template("public/result.html",
                           encode_mp3_file=encode_mp3_file)


@app.route("/get_file/<path:path>")
def get_file(path):
    return send_from_directory(app.config["FILE_FOLDER"], path, as_attachment=True)


def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@app.route("/shutdown", methods=["GET"])
def shutdown():
    shutdown_server()
    return "Server shutting down..."
