from flask import current_app as app
from datetime import datetime
from werkzeug.utils import secure_filename
import os

"""
Saves file and returns its path
"""
def save_file(file) -> str:
    filename = secure_filename(file.filename)
    # get file extension
    _, ext = os.path.splitext(filename)
    # get current timestamp
    timestamp = str(datetime.now().timestamp()).replace('.', '_')
    # create a new filename
    filename = f'{timestamp}{ext}'
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    return path