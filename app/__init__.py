import logging
import os

from flask import Flask
from dotenv import load_dotenv

from app import views, admin_views

load_dotenv()

ALLOWED_EXTENSIONS = {"txt", "wav"}  # txt for phrase_file, wav for mix file
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # max file upload file size ~ 50MB

app = Flask(__name__)

app.config["FILE_FOLDER"] = os.getenv("APG_FILE_FOLDER")
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

logging.basicConfig(filename='flask.log', level=logging.WARN, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
