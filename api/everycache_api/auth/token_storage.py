from flask_jwt_extended.utils import decode_token
from contextlib import contextmanager
from datetime import datetime

from everycache_api.extensions import redis_client
from everycache_api.models import RefreshToken


def load_tokens_from_db(app):
    """Get refresh tokens from db and load them to redis."""
    app.logger.info("Loading tokens from db to redis...")
    tokens = RefreshToken.query.filter(
        RefreshToken.expires > datetime.now()).filter(
        RefreshToken.revoked == 0).all()

    with bulk_redis_operation() as pipeline:
        for token in tokens:
            _add_db_token_to_redis_storage(token, pipeline)


def _add_db_token_to_redis_storage(token, pipeline=None):
    _add_token_to_redis_storage(
        token.jti, token.user_id, "refresh", token.expires, pipeline)


def add_token_to_redis_storage(encoded_token, identity_claim, pipeline=None):
    decoded_token = decode_token(encoded_token)

    jti = decoded_token["jti"]
    user_id = decoded_token[identity_claim]
    token_type = decoded_token["type"]
    expires = datetime.fromtimestamp(decoded_token["exp"])

    _add_token_to_redis_storage(jti, user_id, token_type, expires, pipeline)


def _add_token_to_redis_storage(jti, user_id, token_type, expires, pipeline=None):
    token_key = _get_token_string(jti, user_id, token_type)

    redis_push_obj = pipeline or redis_client
    redis_push_obj.set(token_key, "noop".encode())
    redis_push_obj.expire(token_key, (expires - datetime.now()).seconds)


def get_token_key(jti):
    return next(iter(redis_client.keys(f"jwt_token*jti-{jti}*")), None)


def get_user_token_key(jti, user_id):
    return next(iter(redis_client.keys(f"jwt_token*user_id-{user_id}*jti-{jti}*")), None)


def get_user_token_keys(user_id):
    return redis_client.keys(f"jwt_token*user_id-{user_id}*")


def delete_token(key, pipeline=None):
    pipeline = pipeline or redis_client
    pipeline.delete(key)


@contextmanager
def bulk_redis_operation():
    pipeline = redis_client.pipeline()
    try:
        yield pipeline
    finally:
        pipeline.execute()


def _get_token_string(jti, user_id, token_type):
    return f"jwt_token:user_id-{user_id}:{token_type}:jti-{jti}".encode()
