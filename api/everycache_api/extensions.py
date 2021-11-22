from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from hashids import Hashids
from passlib.context import CryptContext

from everycache_api.common.apispec import APISpecExt
from everycache_api.config import HASHIDS_ALPHABET, HASHIDS_SALT, REDIS_URL

db = SQLAlchemy()
migrate = Migrate()
hashids = Hashids(alphabet=HASHIDS_ALPHABET, salt=HASHIDS_SALT, min_length=8)

ma = Marshmallow()
apispec = APISpecExt()

jwt = JWTManager()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

if REDIS_URL:
    redis_client = FlaskRedis()
else:
    redis_client = False
