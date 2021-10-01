from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from passlib.context import CryptContext

from everycache_api.common.apispec import APISpecExt

db = SQLAlchemy()
migrate = Migrate()

ma = Marshmallow()
apispec = APISpecExt()

jwt = JWTManager()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

redis_client = FlaskRedis()
