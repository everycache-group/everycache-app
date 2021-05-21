from celery import Celery
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from hashids import Hashids
from passlib.context import CryptContext

from everycache_api.commons.apispec import APISpecExt
from everycache_api.config import HASHIDS_SALT

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

hashids = Hashids(salt=HASHIDS_SALT, min_length=32)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
jwt = JWTManager()

apispec = APISpecExt()

celery = Celery()
