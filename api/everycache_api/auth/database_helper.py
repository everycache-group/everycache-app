from sqlalchemy.orm.exc import NoResultFound

from everycache_api.extensions import db
from everycache_api.models import Token, User


def _get_token(user_identity, token_type, jti):  # raises NoResultFound
    return Token.query.filter_by(
        user_id=user_identity, token_type=token_type, jti=jti
    ).one()


def save_token(token: Token):
    db.session.add(token)
    db.session.commit()


def is_token_revoked(user_identity, token_type, jti):
    try:
        token = _get_token(user_identity, token_type, jti)
    except NoResultFound:
        return True
    else:
        return token.revoked


def revoke_token(user_identity, token_type, jti):
    try:
        token = _get_token(user_identity, token_type, jti)
    except NoResultFound:
        return False
    else:
        token.revoked = True

        db.session.commit()

    return True


def revoke_all_user_tokens(user: User):
    tokens = Token.query.filter_by(user=user, revoked=False).all()

    if tokens:
        for token in tokens:
            token.revoked = True

        db.session.commit()

    return True
