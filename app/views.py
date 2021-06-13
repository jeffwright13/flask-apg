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

#THIS IS THE ONE TO USE WHEN APG 1.6.1 IS PUSHED TO MAIN AND PYPI
# import audio_program_generator.apg as apg
import apg

app = create_app()


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

    # Instantiate AudioProgramGenerator object with params passed
    # in from HTML form
    if to_mix:
        p = StringIO(req_phrase_file_obj.read().decode())
        s = BytesIO(req_sound_file_obj.read())
        A = apg.AudioProgramGenerator(
            p,
            s,
            attenuation,
        )
    else:
        p = StringIO(req_phrase_file_obj.read().decode())
        A = apg.AudioProgramGenerator(p)

    # Generate mixed sound file from speech, then serve in browser
    result = A.invoke()
    return send_file(
        result,
        mimetype="audio/mpeg",
        attachment_filename=str(Path(req_phrase_file_obj.filename)),
        as_attachment=True,
    )


"""
@app.route("/get_file/<path:path>")
def get_file(path):
    return send_from_directory(app.config["FILE_FOLDER"],
                               path, as_attachment=True)
"""


def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@app.route("/shutdown", methods=["GET"])
def shutdown():
    shutdown_server()
    return "Server shutting down..."
