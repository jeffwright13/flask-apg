import logging
from pathlib import Path
import os
import sys

from flask import Flask
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", False)

#<<<<<<< HEAD
#from app import views
#=======
#>>>>>>> origin

def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
    app.config["PHRASEFILE_EXTENSIONS"] = {".txt"}
    app.config["SOUNDFILE_EXTENSIONS"] = {".wav"}
    app.config["DEBUG"] = DEBUG
    # TODO: remove this when the memory solution works
    app.config["FILE_FOLDER"] = os.getenv("APG_FILE_FOLDER")
    try:
        Path(app.config["FILE_FOLDER"]).mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    return app


logging_settings = dict(
    filename="flask.log",
    level=logging.WARN,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)
if DEBUG:
    # in debugging (local dev) mode, send logs to standard output
    del logging_settings["filename"]
    logging_settings["stream"] = sys.stdout

logging.basicConfig(**logging_settings)
