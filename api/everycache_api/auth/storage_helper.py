from contextlib import contextmanager
from datetime import datetime
from typing import List

from everycache_api.extensions import redis_client
from everycache_api.models import Token, User


@contextmanager
def _bulk_redis_operation():
    pipeline = redis_client.pipeline()
    try:
        yield pipeline
    finally:
        pipeline.execute()


def _format_token_key(user_id, token_type, jti):
    return f"jwt_token:user_id-{user_id}:{token_type}:jti-{jti}".encode()


def _delete_key(key, pipeline=redis_client):
    return pipeline.delete(key)


def save_token(token: Token, pipeline=redis_client):
    token_key = _format_token_key(token.user.ext_id, token.token_type, token.jti)

    pipeline.set(token_key, "noop".encode())
    pipeline.expire(token_key, (token.expires - datetime.now()).seconds)

    return True


def save_multiple_tokens(tokens: List[Token]):
    with _bulk_redis_operation() as pipeline:
        for token in tokens:
            save_token(token, pipeline)

    return True


def is_token_revoked(user_id, token_type, jti):
    key = _format_token_key(user_id, token_type, jti)

    return redis_client.get(key) is None


def revoke_token(user_id, token_type, jti):
    key = _format_token_key(user_id, token_type, jti)

    return _delete_key(key)


def revoke_all_user_tokens(user: User):
    keys = redis_client.keys(f"jwt_token:user_id-{user.ext_id}:*")

    with _bulk_redis_operation() as pipeline:
        for key in keys:
            _delete_key(key, pipeline)

    return True
