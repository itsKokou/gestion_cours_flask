#Tout ce qui est partagé entre les pages : footer
import os

DEBUG=1

APP_NAME = "KOKOU"

basedir = os.path.abspath(os.path.dirname(__file__))

basedir = basedir.replace("\\config","") # sortir du config

print(basedir)

IMG_FOLDER = basedir + '\src\static\img'

SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir,"inscription.sqlite")

SQLALCHEMY_TRACKMODIFICATIONS = False

SECRET_KEY = "voicimaclesecrete"

NO_IMG = "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg"

#Pour les pages suivante
USE_SESSION_FOR_NEXT = True

FLASK_ENV="development"

PYTHONDONTWRITEBYTECODE=1

PER_PAGE = 3

# WTF_CSRF_ENABLED = False

