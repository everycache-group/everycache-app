"""Various helpers for auth. Mainly about tokens blocklisting

Heavily inspired by
https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/blocklist_database.py
"""
from datetime import datetime

from flask_jwt_extended import create_access_token, create_refresh_token, decode_token

from everycache_api.extensions import redis_client
from everycache_api.models import Token, User

from . import database_helper as db_helper
from . import storage_helper as redis_helper


def create_jwt_payload(user: User):
    identity = user.ext_id
    claims = {"role": user.role.name}

    return {"identity": identity, "additional_claims": claims}


def create_user_access_token(user: User):
    return create_access_token(**create_jwt_payload(user))


def create_user_refresh_token(user: User):
    return create_refresh_token(**create_jwt_payload(user))


def save_encoded_token(encoded_token):
    decoded_token = decode_token(encoded_token)

    jti = decoded_token["jti"]
    token_type = decoded_token["type"]
    user = User.query_ext_id(decoded_token["sub"]).one()
    expires = datetime.fromtimestamp(decoded_token["exp"])
    revoked = False

    token = Token(
        jti=jti,
        token_type=token_type,
        user=user,
        expires=expires,
        revoked=revoked,
    )

    if redis_client:
        redis_helper.save_token(token)

    if token_type == "refresh" or not redis_client:
        # if redis is used, only refresh tokens are saved in database
        db_helper.save_token(token)

    return True


def is_token_revoked(jwt_payload):
    """
    Checks if the given token is revoked or not. Because we are saving all tokens we
    create, if the token is not found, it is consider revoked
    """
    user_id = jwt_payload["sub"]
    token_type = jwt_payload["type"]
    jti = jwt_payload["jti"]

    if redis_client:
        return redis_helper.is_token_revoked(user_id, token_type, jti)
    else:
        return db_helper.is_token_revoked(user_id, token_type, jti)


def revoke_token(jwt_payload):
    if is_token_revoked(jwt_payload):
        raise Exception("Token is already revoked")

    jti = jwt_payload["jti"]
    user_id = jwt_payload["sub"]
    token_type = jwt_payload["type"]

    if redis_client:
        redis_helper.revoke_token(user_id, token_type, jti)

    if token_type == "refresh" or not redis_client:
        # if redis is used, only refresh tokens are saved in database
        db_helper.revoke_token(user_id, token_type, jti)


def revoke_all_user_tokens(user: User):
    if redis_client:
        redis_helper.revoke_all_user_tokens(user)

    db_helper.revoke_all_user_tokens(user)

    return True
