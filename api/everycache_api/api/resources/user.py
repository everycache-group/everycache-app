from flask import request
from flask_jwt_extended import get_current_user, get_jwt_identity, jwt_required
from flask_restful import Resource

from everycache_api.api.schemas import UserSchema
from everycache_api.common.pagination import paginate
from everycache_api.extensions import db, ma
from everycache_api.models import User


class UserResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: username
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: UserSchema
        404:
          description: user does not exist
      security: []
    """

    def get(self, username: str):

        schema = UserSchema()
        user = User.query.filter_by(username=username).first_or_404()

        return {"user": schema.dump(user)}


# class UserDetailsResource(Resource):
#     # method_decorators = [jwt_required()]

#     def get(self, username: str):
#         schema = UserDetailsSchema()
#         user = User.query.filter_by(username=username).first_or_404()

#         return {"user": schema.dump(user)}


# class CurrentUserDetailsResource(Resource):
#     """Single object resource

#     ---
#     get:
#       tags:
#         - api
#       responses:
#         200:
#           content:
#             application/json:
#               schema:
#                 type: object
#                 properties:
#                   user: CurrentUserDetailsSchema
#     put:
#       tags:
#         - api
#       requestBody:
#         content:
#           application/json:
#             schema:
#               CurrentUserDetailsSchema
#       responses:
#         200:
#           content:
#             application/json:
#               schema:
#                 type: object
#                 properties:
#                   msg:
#                     type: string
#                     example: user updated
#                   user: CurrentUserDetailsSchema
#     """

#     method_decorators = [jwt_required()]

#     def get(self, username: str):
#         schema = CurrentUserDetailsSchema()
#         user = User.query.filter_by(username=username).first_or_404()

#         return {"user": schema.dump(user)}

#     def put(self, username: str):
#         schema = CurrentUserDetailsSchema()
#         user = User.query.filter_by(username=username).first_or_404()

#         user = schema.load(request.json, instance=user)

#         db.session.commit()

#         return {"msg": "user updated", "user": schema.dump(user)}

#     def delete(self, username: str):
#         user = User.query.filter_by(username=username).first_or_404()

#         user.active = False

#         db.session.commit()

#         return {"msg": "user deleted"}


class UserList(Resource):
    """Multiple objects resource

    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/UserSchema'
    """

    method_decorators = {"get": [jwt_required(optional=True)], "post": [jwt_required()]}

    def get(self):
        user = get_current_user()
        if user:
            if user.role == User.Role.admin:
                return "admin"
            elif user.role == User.Role.default:
                return "default"

        schema = UserSchema(many=True)
        query = User.query

        return paginate(query, schema)

    def post(self):
        schema = UserSchema()
        user = schema.load(request.json)

        db.session.add(user)
        db.session.commit()

        return {"msg": "user created", "user": schema.dump(user)}, 201
