from everycache_api.users.helpers import add_user
from everycache_api.api.schemas.user import UserSchema
from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource
from everycache_api.extensions import db
from sqlalchemy.exc import IntegrityError

from everycache_api.api.schemas import ProfileSchema


class ProfileResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: ProfileSchema
    """

    method_decorators = {
        "get": [jwt_required()],
        "put": [jwt_required()],
    }

    def get(self):
        schema = ProfileSchema()
        return {"user": schema.dump(current_user)}

    def put(self):
        schema = ProfileSchema()
        schema.load(request.json, instance=current_user, partial=True)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

        db.session.refresh(current_user)

        return {"user": schema.dump(current_user)}

    def post(self):
        """Creating a new account"""
        schema = ProfileSchema()
        return add_user(schema)
