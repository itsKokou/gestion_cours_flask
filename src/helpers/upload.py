from app import app
from werkzeug.utils import secure_filename
import os


def uploadPhoto(photo,matricule):
    filename = secure_filename(f"{matricule}{os.path.splitext(photo.filename)[1]}").lower()
    filepath = os.path.join(app.config['IMG_FOLDER'], filename)
    photo.save(filepath)
    return filename