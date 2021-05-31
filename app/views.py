from flask import render_template, request, jsonify
from datetime import datetime
from app import app



import sys
import math
from pathlib import Path
from gtts import gTTS
from pydub import AudioSegment

@app.route("/setvals", methods=("GET", "POST"))
def setvals():
    if request.method == 'POST':
        phrase_file = request.form.get("phrase_file")
        to_mix = request.form.get("to_mix")
        sound_file = request.form.get("sound_file")
        attenuation = request.form.get("attenuation")

        return jsonify(
            {
                "phrase_file": phrase_file,  # "test.txt"
                "to_mix": to_mix,            # "on" or null
                "sound_file": sound_file,    # "birds.wav"
                "attenuation": attenuation,  # "33"
            }
        )


        #return run_apg()
    else:
        return render_template("public/setvals.html")

@app.route("/run_apg", methods=["GET", "POST"])
def run_apg():
    phrase_file = request.args.get("phrase_file", None)
    to_mix = request.args.get("to_mix", False)
    sound_file = request.args.get("sound_file", None)
    attenuation = request.args.get("attenuation", 0)

    '''
    A = Apg(phrase_file, to_mix, sound_file, attenuation)
    A.gen_speech()

    if A.to_mix == True:
        bkgnd = AudioSegment.from_file(A.sound_file, format="wav")
        A.mix_file = A.mix(A.speech_file, bkgnd, A.attenuation)
        A.mix_file.export(A.save_file, format="mp3")
    else:
        A.speech_file.export(A.save_file, format="mp3")

    return jsonify(
        {
            "phrase_file": A.phrase_file,
            "save_file": A.save_file,
            "to_mix": A.to_mix,
            "sound_file": A.sound_file,
            "attenuation": A.attenuation,
        }
    )
    '''
    return jsonify(
        {
            "phrase_file": phrase_file,
            "to_mix": to_mix,
            "sound_file": sound_file,
            "attenuation": attenuation,
        }
    )



@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

@app.route("/")
@app.route("/index")
def index():
    return render_template("public/index.html")

@app.route("/about")
def about():
    return render_template("public/about.html")

@app.route("/jinja")
def jinja():

    date = datetime.utcnow()

    # Strings
    my_name = "Julian"

    # Integers
    my_age = 30

    # Lists
    langs = ["Python", "JavaScript", "Bash", "Ruby", "C", "Rust"]

    # Dictionaries
    friends = {
        "Tony": 43,
        "Cody": 28,
        "Amy": 26,
        "Clarissa": 23,
        "Wendell": 39
    }

    # Tuples
    colors = ("Red", "Blue")

    # Booleans
    cool = True

    # Classes
    class GitRemote:
        def __init__(self, name, description, domain):
            self.name = name
            self.description = description
            self.domain = domain

        def clone(self, repo):
            return f"Cloning into {repo}"

    my_remote = GitRemote(
        name="Learning Flask",
        description="Learn the Flask web framework for Python",
        domain="https://github.com/Julian-Nash/learning-flask.git"
    )

    # Functions
    def repeat(x, qty=1):
        return x * qty

    return render_template(
        "public/jinja.html", my_name=my_name, my_age=my_age, langs=langs,
        friends=friends, colors=colors, cool=cool, GitRemote=GitRemote,
        my_remote=my_remote, repeat=repeat, date=date
    )
