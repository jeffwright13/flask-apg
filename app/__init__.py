from flask import Flask

FILE_FOLDER = r"/Users/jeff/tmp"  # local folder to store uploaded/generated files
ALLOWED_EXTENSIONS = {"txt", "wav"}  # txt for phrase_file, wav for mix file
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # max file upload file size ~ 50MB

app = Flask(__name__)

app.config["FILE_FOLDER"] = FILE_FOLDER
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

from app import views
from app import admin_views

import logging

logging.basicConfig(
    filename="flask.log",
    level=logging.WARN,
    format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)
