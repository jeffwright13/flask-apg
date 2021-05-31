from flask import Flask

UPLOAD_FOLDER = r"/Users/Jeff/tmp"     # local folder to store uploaded files
ALLOWED_EXTENSIONS = {'txt', "wav"}    # txt for phrase_file, wav for mix file
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # max file upload file size ~ 50MB

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

from app import views
from app import admin_views
