from pathlib import Path

from flask import (
    render_template,
    request,
    redirect,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

from app import create_app
import audio_program_generator.apg as apg


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

    # Instantiate AudioProgramGenerator object with params passed
    # in from HTML form
    if to_mix:
        A = apg.AudioProgramGenerator(
            phrase_file,
            to_mix,
            sound_file,
            attenuation,
        )
    else:
        A = apg.AudioProgramGenerator(
            phrase_file,
        )

    # Generate mixed sound file from speech, then serve in browser
    A.invoke()
    # return redirect(url_for("get_file", path=Path(A.save_file).name))
    return get_file(path=Path(A.save_file).name)


@app.route("/get_file/<path:path>")
def get_file(path):
    return send_from_directory(app.config["FILE_FOLDER"],
                               path, as_attachment=True)


def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@app.route("/shutdown", methods=["GET"])
def shutdown():
    shutdown_server()
    return "Server shutting down..."


@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin/dashboard.html")


@app.route("/admin/profile")
def admin_profile():
    return render_template("admin/profile.html")
