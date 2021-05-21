from datetime import datetime

from flask_jwt_extended import decode_token
from sqlalchemy.orm.exc import NoResultFound

from everycache_api.extensions import db
from everycache_api.models.auth_token import AuthToken


def add_token_to_database(encoded_token, identity_claim):
    decoded_token = decode_token(encoded_token)
    jti = decoded_token["jti"]
    token_type = decoded_token["type"]
    user_id = decoded_token[identity_claim]
    expires = datetime.fromtimestamp(decoded_token["exp"])
    revoked = False

    db_token = AuthToken(
        jti=jti,
        token_type=token_type,
        user_id=user_id,
        expires=expires,
        revoked=revoked,
    )
    db.session.add(db_token)
    db.session.commit()


def is_token_revoked(jwt_payload):
    jti = jwt_payload["jti"]
    try:
        token = AuthToken.query.filter_by(jti=jti).one()
    except NoResultFound:
        return True
    else:
        return token.revoked


def revoke_token(token_jti, user):
    try:
        token = AuthToken.query.filter_by(jti=token_jti, user=user).one()
    except NoResultFound:
        raise Exception(f"Could not find the auth token {token_jti}")
    else:
        token.revoked = True
        db.session.commit()
