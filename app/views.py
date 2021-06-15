import logging
from pathlib import Path
from io import StringIO, BytesIO, TextIOWrapper

from flask import (
    render_template,
    request,
    redirect,
    send_file,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

from app import create_app

# import apg  ## Use when debuggging and copy apg.py to root repo dir
import audio_program_generator.apg as apg

app = create_app()


@app.route("/", methods=("GET", "POST"))
def setvals():
    # All requests other than POST (i.e. GET) are re-shown the input form.
    if not request.method == "POST":
        return render_template("public/setvals.html")

    # Local handles for request object (type: Werkzeug FileStorage)
    req_phrase_file_obj = request.files["phrase_file"]
    req_sound_file_obj = request.files["sound_file"]

    # Verify phrase_file type is allowed; if not, redirect to input form.
    if (
        Path(req_phrase_file_obj.filename).suffix
        not in app.config["PHRASEFILE_EXTENSIONS"]
    ):
        return render_template("public/setvals.html")

    # Instantiate AudioProgramGenerator object with params passed
    # in from HTML form
    slow = True if request.form.get("slow") == "on" else False
    attenuation = request.form.get("attenuation")
    kwargs = dict(slow=slow, attenuation=attenuation)
    phr = StringIO(req_phrase_file_obj.read().decode())
    snd = None if req_sound_file_obj.filename == '' else BytesIO(req_sound_file_obj.read())
    A = apg.AudioProgramGenerator(
        phr,
        snd,
        **kwargs,
    )

    # Generate mixed sound file from speech, then serve in browser
    result = A.invoke()
    return send_file(
        result,
        mimetype="audio/mpeg",
        attachment_filename=str(Path(req_phrase_file_obj.filename)),
        as_attachment=True,
    )

def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@app.route("/shutdown", methods=["GET"])
def shutdown():
    shutdown_server()
    return "Server shutting down..."
