from flask import request
from everycache_api.extensions import db
from sqlalchemy.exc import IntegrityError


def add_user(schema):
    user = schema.load(request.json)

    if not add_user_to_db(user):
        return {"msg": "user of this data already exists"}, 400

    return {"msg": "user created", "user": schema.dump(user)}, 201


def add_user_to_db(user):
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        return False
    return True
