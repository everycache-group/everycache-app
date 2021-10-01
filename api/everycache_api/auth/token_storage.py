from flask_jwt_extended.utils import decode_token
import isodate
from contextlib import contextmanager
from datetime import datetime
from everycache_api.extensions import redis_client
from everycache_api.models import Token


def load_tokens_from_db(app):
    """Get refresh tokens from db and load them to redis."""
    app.logger.info("Loading tokens from db to redis...")
    tokens = Token.query.filter(
        Token.expires > datetime.now()).filter(
        Token.revoked == 0).all()

    with bulk_redis_operation() as pipeline:
        for token in tokens:
            _add_db_token_to_redis_storage(token, pipeline)


def _add_db_token_to_redis_storage(token, pipeline=None):
    _add_token_to_redis_storage(
        token.jti, {"token_type": "refresh".encode(), **_encode_db_token_struct(token)},
        token.expires, pipeline)


def add_token_to_redis_storage(encoded_token, identity_claim, pipeline=None):
    decoded_token = decode_token(encoded_token)

    jti = decoded_token["jti"]
    expires = datetime.fromtimestamp(decoded_token["exp"])

    token_data = {
        "token_type": decoded_token["type"],
        "user_id": decoded_token[identity_claim],
        "expires": expires,
        "revoked": False
    }
    for key, value in dict(token_data).items():
        token_data[key] = _encode_field(key, value)

    _add_token_to_redis_storage(jti, token_data, expires, pipeline)


def _add_token_to_redis_storage(jti, token_data, expires, pipeline=None):
    token_key = _get_token_string(jti)
    token_user_id = token_data["user_id"]

    redis_push_obj = pipeline or redis_client
    redis_push_obj.hset(token_key, mapping=token_data)
    redis_push_obj.expire(token_key, (expires - datetime.now()).seconds)

    redis_push_obj.sadd(_get_user_token_string(token_user_id), jti)


def get_token_data(jti, keys=("token_type", "user_id", "revoked", "expires")):
    """Get token_data dict from redis. The output is automatically decoded into python types."""
    data = _get_token_data_from_redis(jti, keys)

    # assume that no element can be None - if the approach is invalid use:
    # `if all(map(lambda x: x is None, data))`
    if next(iter(data.values())) is None:
        return None
    return data


def set_token_field(jti, key, value, pipeline=None):
    """Set token field value in redis."""
    redis_push_obj = pipeline or redis_client
    encoded_value = _encode_field(key, value)
    redis_push_obj.hset(_get_token_string(jti), key=key, value=encoded_value)


def revoke_all_user_tokens_redis(user_id):
    """Remove each token from the user-tokens redis' set and mark each token as revoked."""
    user_redis_key = _get_user_token_string(user_id)
    size = redis_client.scard(user_redis_key)
    jtis = redis_client.spop(user_redis_key, size)

    with bulk_redis_operation() as pipeline:
        for jti in jtis:
            if get_token_data(jti) != None:
                set_token_field(jti, "revoked", True, pipeline)


@contextmanager
def bulk_redis_operation():
    pipeline = redis_client.pipeline()
    try:
        yield pipeline
    finally:
        pipeline.execute()


def _encode_field(key, value):
    if key in ("user_id", "revoked"):
        return str(value)
    elif key == "expires":
        return value.isoformat()
    return value


def _encode_db_token_struct(token):
    keys = ("user_id", "revoked", "expires")
    return dict(zip(keys, map(lambda x: _encode_field(x, getattr(token, x, "")), keys)))


def _decode_field(key, value):
    if key == "user_id":
        return int(value)
    elif key == "revoked":
        return value.lower() in ("true", "1")
    elif key == "expires":
        return isodate.parse_datetime(value.decode())
    elif key == "token_type":
        return value.decode()

    return value


def _get_token_data_from_redis(jti, keys):
    data = redis_client.hmget(_get_token_string(jti), keys)
    encoded_data = dict(zip(keys, data))
    data = dict(encoded_data)
    for key, value in encoded_data.items():
        if value is None:
            data[key] = value
            continue
        data[key] = _decode_field(key, value)

    return data


def _get_token_string(jti):
    return f"jwt_token:{jti}".encode()


def _get_user_token_string(user_id):
    return f"user_tokens:{user_id}".encode()
