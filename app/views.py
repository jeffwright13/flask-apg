import os
from pathlib import Path

from flask import (
    render_template,
    request,
    redirect,
    jsonify,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

from pydub import AudioSegment

from app import app
import app.apg as apg


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/setvals", methods=("GET", "POST"))
def setvals():
    # All requests other than POST (i.e. GET) are shown the input form.
    # Data from the form's 'submit' button result in a POST, and will be
    # processed by the audio_program_generator (apg) code.

    if not request.method == "POST":
        return render_template("public/setvals.html")
    else:
        to_mix = True if request.form.get("to_mix") == "on" else False

        # Verify phrase_file type is allowed; if not, redirect to form page.
        phrase_file = request.files["phrase_file"]
        if not allowed_file(phrase_file.filename):
            return render_template("public/setvals.html")
        else:
            Path(app.config["FILE_FOLDER"]).mkdir(parents=True, exist_ok=True)
            phrase_savefile = secure_filename(phrase_file.filename)
            phrase_file.save(
                os.path.join(app.config["FILE_FOLDER"], phrase_savefile)
            )  # CONVERT ME TO PATHLIB!
            phrase_file.close()

        if to_mix:
            # breakpoint()
            attenuation = int(request.form.get("attenuation"))
            sound_file = request.files["sound_file"]
            if not allowed_file(sound_file.filename):
                return render_template("public/setvals.html")
            else:
                sound_savefile = secure_filename(sound_file.filename)
                sound_file.save(os.path.join(app.config["FILE_FOLDER"], sound_savefile))  # CONVERT ME TO PATHLIB!
                sound_file.close()

        if to_mix:
            A = apg.Apg(
                os.path.join(app.config["FILE_FOLDER"], phrase_savefile),
                to_mix,
                os.path.join(app.config["FILE_FOLDER"], sound_savefile),
                attenuation,
            )  # CONVERT ME TO PATHLIB!
        else:
            A = apg.Apg(os.path.join(app.config["FILE_FOLDER"], phrase_savefile))  # CONVERT ME TO PATHLIB!

        A.gen_speech()

        # TODO: abstract out into the class?
        if A.to_mix == True:
            bkgnd = AudioSegment.from_file(A.sound_file, format="wav")
            A.mix_file = A.mix(A.speech_file, bkgnd, A.attenuation)
            A.mix_file.export(A.save_file, format="mp3")
        else:
            A.speech_file.export(A.save_file, format="mp3")

        # return render_template("public/download_file.html", filename=A.save_file)
        return redirect(url_for("get_file", path=Path(A.save_file).name))


@app.route("/get_file/<path:path>")
def get_file(path):
    """Download a file."""
    app.logger.debug("path: ", path)
    return send_from_directory(app.config["FILE_FOLDER"], path, as_attachment=True)
