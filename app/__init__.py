from flask import Flask
from pathlib import Path

FILE_FOLDER = r"/Users/jeff/tmp"  # local folder to store uploaded/generated files
PHRASEFILE_EXTENSIONS = {".txt"}  # txt for phrase_file, wav for mix file
SOUNDFILE_EXTENSIONS = {".wav"}  # txt for phrase_file, wav for mix file
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # max file upload file size ~ 50MB

app = Flask(__name__)

app.config["FILE_FOLDER"] = FILE_FOLDER
app.config["PHRASEFILE_EXTENSIONS"] = PHRASEFILE_EXTENSIONS
app.config["SOUNDFILE_EXTENSIONS"] = SOUNDFILE_EXTENSIONS
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

from app import views
from app import admin_views

# Config app for file upload location, and create dir if needed
Path(app.config["FILE_FOLDER"]).mkdir(parents=True, exist_ok=True)

import logging

logging.basicConfig(
    filename="flask.log",
    level=logging.WARN,
    format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)
