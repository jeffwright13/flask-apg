from base64 import b64encode
from pathlib import Path

from flask import render_template, request

from app import app

from app.tasks import create_audio_mix


@app.route("/", methods=("GET", "POST"))
def setvals():
    # All requests other than POST (i.e. GET) are re-shown the input form.
    if not request.method == "POST":
        return render_template("public/setvals2.html")

    # Local handles for request object (type: Werkzeug FileStorage)
    req_phrase_file_obj = request.files["phrase_file"]
    req_sound_file_obj = request.files.get("sound_file", None)

    # Verify phrase_file type is allowed; if not, redirect to input form.
    if (
        Path(req_phrase_file_obj.filename).suffix
        not in app.config["PHRASEFILE_EXTENSIONS"]
    ):
        return render_template("public/setvals.html")

    # Verify sound_file type is allowed; if not, redirect to input form.
    if req_sound_file_obj and (
        Path(req_sound_file_obj.filename).suffix
        not in app.config["SOUNDFILE_EXTENSIONS"]
    ):
        return render_template("public/setvals.html")

    kwargs = dict(
        attenuation=int(request.form.get("attenuation", 0))
    )

    req_phrase_file_content_encoded = b64encode(
        req_phrase_file_obj.read())
    req_sound_file_content_encoded = b64encode(
        req_sound_file_obj.read())

    create_audio_mix.delay(
        req_phrase_file_obj.filename,
        req_phrase_file_content_encoded,
        req_sound_file_obj.filename,
        req_sound_file_content_encoded,
        **kwargs)


    return render_template("public/setvals.html",
                           msg="Your file is processing")


def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@app.route("/shutdown", methods=["GET"])
def shutdown():
    shutdown_server()
    return "Server shutting down..."
