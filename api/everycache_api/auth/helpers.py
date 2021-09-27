"""Various helpers for auth. Mainly about tokens blocklisting

Heavily inspired by
https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/blocklist_database.py
"""
from datetime import datetime

from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from sqlalchemy.orm.exc import NoResultFound

from everycache_api.extensions import db
from everycache_api.models import Token, User


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
    token_type = decoded_token["type"]
    user_identity = decoded_token[identity_claim]
    expires = datetime.fromtimestamp(decoded_token["exp"])
    revoked = False

    db_token = Token(
        jti=jti,
        token_type=token_type,
        user_id=user_identity,
        expires=expires,
        revoked=revoked,
    )
    db.session.add(db_token)
    db.session.commit()


def is_token_revoked(jwt_payload):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = jwt_payload["jti"]
    try:
        token = Token.query.filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True


def revoke_token(token_jti, user_identity):
    """Revokes the given token

    Since we use it only on logout that already require a valid access token,
    if token is not found we raise an exception
    """
    try:
        token = Token.query.filter_by(jti=token_jti, user_id=user_identity).one()
        token.revoked = True
        db.session.commit()
    except NoResultFound:
        raise Exception(f"Could not find the token {token_jti}")


def revoke_all_user_tokens(user):
    tokens = Token.query.filter_by(user=user).all()

    if not tokens:
        return False

    for token in tokens:
        token.revoked = True

    db.session.commit()

    return True
