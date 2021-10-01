from os import getenv

from dotenv import load_dotenv

load_dotenv()

ENV = getenv("FLASK_ENV")
DEBUG = ENV == "development" or getenv("DEBUG", "").lower() in ["true", "1"]

SECRET_KEY = getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI", "sqlite:///dev.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

HASHIDS_ALPHABET = getenv("HASHIDS_ALPHABET", "abcdefghijklmnopqrstuvwxyz")
HASHIDS_SALT = getenv("HASHIDS_SALT")

# jwt access and refresh tokens validity times in minutes
JWT_ACCESS_TOKEN_EXPIRES = int(getenv("JWT_ACCESS_TOKEN_EXPIRY_MINUTES", "15")) * 60
JWT_REFRESH_TOKEN_EXPIRES = int(getenv("JWT_REFRESH_TOKEN_EXPIRY_MINUTES", "720")) * 60
