import logging
from pathlib import Path

from flask import render_template, request

from app import app
from .aws import create_audio_mix


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

    response = create_audio_mix(
        req_phrase_file_obj,
        req_sound_file_obj,
        **kwargs)

    file = response.get("result_file")
    exception = response.get("exception")
    status_code = response.get("status_code")
    message = response.get("message")

    if status_code == 200:
        logging.debug(
            f"AWS generated mix file: {file}")
    # sometimes lambda returns something app developer did not define,
    # e.g. {'message': 'Endpoint request timed out'}
    elif message:
        logging.error(
            ("AWS failed to generate mix file, "
             f"message returned: {message}"))
    else:
        logging.error(
            ("AWS failed to generate mix file, "
             f"exception: {exception}"))

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
