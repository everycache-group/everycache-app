from os import getenv

from dotenv import load_dotenv


def getenv_bool(env_var_name: str) -> bool:
    return getenv(env_var_name, "").lower in ["true", "1"]


load_dotenv()

ENV = getenv("FLASK_ENV")
DEBUG = ENV == "development" or getenv_bool("DEBUG")

SECRET_KEY = getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI", "sqlite:///dev.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

HASHIDS_ALPHABET = getenv("HASHIDS_ALPHABET", "abcdefghijklmnopqrstuvwxyz")
HASHIDS_SALT = getenv("HASHIDS_SALT")

# jwt access and refresh tokens validity times in minutes
JWT_ACCESS_TOKEN_EXPIRES = int(getenv("JWT_ACCESS_TOKEN_EXPIRY_MINUTES", "15")) * 60
JWT_REFRESH_TOKEN_EXPIRES = int(getenv("JWT_REFRESH_TOKEN_EXPIRY_MINUTES", "720")) * 60

REDIS_URL = getenv("REDIS_URL")
FRONTEND_APP_URL = getenv("FRONTEND_APP_URL", "http://localhost:3000")
