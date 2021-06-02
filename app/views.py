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

from app import app
import app.apg as apg


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/setvals", methods=("GET", "POST"))
def setvals():

    # All requests other than POST (i.e. GET) are re-shown the input form.
    if not request.method == "POST":
        return render_template("public/setvals2.html")
    else:
        to_mix = True if request.form.get("to_mix") == "on" else False

        # Verify phrase_file type is allowed; if not, redirect to form page.
        phrase_file = request.files["phrase_file"]
        if not allowed_file(phrase_file.filename):
            return render_template("public/setvals.html")
        else:
            # Config app for file upload ocaion, and create dir if needed
            Path(app.config["FILE_FOLDER"]).mkdir(parents=True, exist_ok=True)

            # Save the phrase file to local file upload dir
            phrase_savefile = secure_filename(phrase_file.filename)
            phrase_file.save(
                os.path.join(app.config["FILE_FOLDER"], phrase_savefile)
            )  # CONVERT ME TO PATHLIB!
            phrase_file.close()

        if to_mix:
            attenuation = (
                int(request.form.get("attenuation"))
                if request.form.get("attenuation")
                else 0
            )
            sound_file = request.files["sound_file"]
            if not allowed_file(sound_file.filename):
                return render_template("public/setvals.html")
            else:
                sound_savefile = secure_filename(sound_file.filename)
                sound_file.save(
                    os.path.join(app.config["FILE_FOLDER"], sound_savefile)
                )  # CONVERT ME TO PATHLIB!
                sound_file.close()

        if to_mix:
            A = apg.Apg(
                os.path.join(app.config["FILE_FOLDER"], phrase_savefile),
                to_mix,
                os.path.join(app.config["FILE_FOLDER"], sound_savefile),
                attenuation,
            )  # CONVERT ME TO PATHLIB!
        else:
            A = apg.Apg(
                os.path.join(app.config["FILE_FOLDER"], phrase_savefile)
            )  # CONVERT ME TO PATHLIB!

        A.gen_speech()
        A.invoke()

        # Refresh page and direct broswer to save/open resultant file
        # (see get_file endpoint directly below)
        return redirect(url_for("get_file", path=Path(A.save_file).name))


@app.route("/get_file/<path:path>")
def get_file(path):
    return send_from_directory(app.config["FILE_FOLDER"], path, as_attachment=True)
