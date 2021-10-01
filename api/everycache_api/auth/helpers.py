"""Various helpers for auth. Mainly about tokens blocklisting

Heavily inspired by
https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/blocklist_database.py
"""
from datetime import datetime

from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from flask_jwt_extended.utils import get_jwt_identity

from everycache_api.extensions import db
from everycache_api.models import Token, User
from everycache_api.auth.token_storage import get_token_data, revoke_all_user_tokens_redis, set_token_field


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

    db_token = Token(
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

    token_data = get_token_data(jti, keys=("revoked",))
    print(token_data)
    if token_data is None:
        return True

    return token_data.get("revoked", False)


def revoke_token(token_jti, user_identity):
    """
    Revokes the given token
    """
    token = Token.query.filter_by(jti=token_jti, user_id=user_identity).first()
    if token is not None:
        token.revoked = True
        db.session.commit()

    token_data = get_token_data(token_jti, ("revoked", "user_id"))
    if token_data["revoked"] or token_data["user_id"] != user_identity:
        return

    set_token_field(token_jti, "revoked", True)


def revoke_all_user_tokens(user):
    tokens = Token.query.filter_by(user=user).all()

    if not tokens:
        return False

    revoke_all_user_tokens_redis(get_jwt_identity())

    for token in tokens:
        token.revoked = True

    db.session.commit()

    return True
