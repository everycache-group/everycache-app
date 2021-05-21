from os import getenv

from dotenv import load_dotenv

load_dotenv()

ENV = getenv("FLASK_ENV")
DEBUG = (ENV == "development") or (getenv("DEBUG", "").lower() in ("true", "1"))
SECRET_KEY = getenv("SECRET_KEY")

HASHIDS_SALT = getenv("HASH_SALT")

SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND_RUL = getenv("CELERY_RESULT_BACKEND_URL")
