from os import getenv

from dotenv import load_dotenv


def getenv_bool(env_var_name: str) -> bool:
    return getenv(env_var_name, "").lower in ["true", "1"]


load_dotenv()

ENV = getenv("FLASK_ENV")
DEBUG = ENV == "development" or getenv_bool("DEBUG")

SECRET_KEY = getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

HASHIDS_ALPHABET = getenv("HASHIDS_ALPHABET", "abcdefghijklmnopqrstuvwxyz")
HASHIDS_SALT = getenv("HASHIDS_SALT")

# jwt access and refresh tokens validity times in minutes
JWT_ACCESS_TOKEN_EXPIRES = int(getenv("JWT_ACCESS_TOKEN_EXPIRY_MINUTES", "15")) * 60
JWT_REFRESH_TOKEN_EXPIRES = int(getenv("JWT_REFRESH_TOKEN_EXPIRY_MINUTES", "720")) * 60

REDIS_URL = getenv("REDIS_URL")
FRONTEND_APP_URL = getenv("FRONTEND_APP_URL", "http://localhost:3000")



MAIL_SERVER = getenv("MAIL_SERVER", 'smtp.gmail.com')
MAIL_PORT = getenv("MAIL_PORT", 465)
MAIL_USERNAME = getenv("MAIL_USERNAME", 'everycache@gmail.com')
MAIL_PASSWORD = getenv("MAIL_PASSWORD", "")
MAIL_USE_TLS = getenv("MAIL_USE_TLS", "false").lower() in ("1", "true")
MAIL_USE_SSL = getenv("MAIL_USE_SSL", "true").lower() in ("1", "true")
