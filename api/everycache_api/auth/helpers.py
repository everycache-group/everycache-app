"""Various helpers for auth. Mainly about tokens blocklisting

Heavily inspired by
https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/blocklist_database.py
"""
from datetime import datetime

from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from flask_jwt_extended.utils import get_jwt_identity

from everycache_api.extensions import db
from everycache_api.models import RefreshToken, User
from everycache_api.auth.token_storage import bulk_redis_operation, delete_token, get_token_key, get_user_token_key, get_user_token_keys


def create_jwt_payload(user: User):
    identity = user.id_
    claims = {"role": user.role.value}

    return {"identity": identity, "additional_claims": claims}


def create_user_access_token(user: User):
    return create_access_token(**create_jwt_payload(user))


def create_user_refresh_token(user: User):
    return create_refresh_token(**create_jwt_payload(user))


def add_token_to_database(encoded_token, identity_claim):
    """
    Adds a new token to the database.

    :param identity_claim: configured key to get user identity
    """
    decoded_token = decode_token(encoded_token)

    jti = decoded_token["jti"]
    user_identity = decoded_token[identity_claim]
    expires = datetime.fromtimestamp(decoded_token["exp"])
    revoked = False

    db_token = RefreshToken(
        jti=jti,
        user_id=user_identity,
        expires=expires,
        revoked=revoked,
    )
    db.session.add(db_token)
    db.session.commit()


def is_token_revoked(jwt_payload):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into redis, if the token is not present
    there we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = jwt_payload["jti"]
    return get_token_key(jti) is None


def revoke_token(token_jti, user_identity):
    """
    Revokes the given token
    """
    token = RefreshToken.query.filter_by(jti=token_jti, user_id=user_identity).first()
    if token is not None:
        token.revoked = True
        db.session.commit()

    delete_token(get_user_token_key(token_jti, user_identity))


def revoke_all_user_tokens(user):
    tokens = RefreshToken.query.filter_by(user=user).all()

    if not tokens:
        return False

    for token in tokens:
        token.revoked = True

    db.session.commit()

    redis_token_keys = get_user_token_keys(get_jwt_identity())
    with bulk_redis_operation as redis_client:
        for token_key in redis_token_keys:
            delete_token(token_key, redis_client)

    return True
