from flask import abort, request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource

from everycache_api.api.schemas import (
    CacheCommentSchema,
    CacheSchema,
    CacheVisitSchema,
    PublicCacheSchema,
    PublicUserSchema,
    UserSchema,
)
from everycache_api.auth.helpers import revoke_all_user_tokens
from everycache_api.common.pagination import paginate
from everycache_api.extensions import db
from everycache_api.models import Cache, CacheComment, CacheVisit, User


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
                  user:
                    oneOf:
                      - UserSchema
                      - PublicUserSchema
        404:
          description: user not found
      security: []
    put:
      tags:
        - api
      parameters:
        - in: path
          name: username
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user updated
                  user:
                    UserSchema
        403:
          description: forbidden
        404:
          description: user not found
    delete:
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
                  msg:
                    type: string
                    example: user deleted
        403:
          description: forbidden
        404:
          description: user not found
    """

    method_decorators = {
        "get": [jwt_required(optional=True)],
        "put": [jwt_required()],
        "delete": [jwt_required()],
    }

    def get(self, username: str):
        # find user
        user = User.query.filter_by(username=username).first_or_404()

        # decide which schema to use
        schema = None
        if current_user and (
            current_user.username == username or current_user.role == User.Role.Admin
        ):
            # user is querying own account info or is an admin
            schema = UserSchema()
        else:
            # user is not logged in or is querying other user's account info
            schema = PublicUserSchema()

        # return user details
        return {"user": schema.dump(user)}, 200

    def put(self, username: str):
        # ensure current_user is authorized
        if current_user.username != username and current_user.role != User.Role.Admin:
            abort(403)

        # find user
        user = User.query.filter_by(username=username).first_or_404()

        schema = UserSchema()

        # update and return user details
        user = schema.load(request.json, instance=user)
        db.session.commit()

        return {"msg": "user updated", "user": schema.dump(user)}, 200

    def delete(self, username: str):
        # ensure current_user is authorized
        if current_user.username != username and current_user.role != User.Role.Admin:
            abort(403)

        # find user
        user = User.query.filter(username=username).first_or_404()

        # mark user as deleted
        user.deleted = True
        db.session.commit()

        # revoke any tokens for deleted user
        revoke_all_user_tokens(user)

        return {"msg": "user deleted"}, 200


class UserListResource(Resource):
    """Multiple objects resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: query
          name: order_by
          schema:
            type: string
          required: false
          description: field to order items by
        - in: query
          name: desc
          schema:
            type: boolean
          allowEmptyValue: true
          required: false
          description: order results descending
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
                          oneOf:
                            - $ref: '#/components/schemas/UserSchema'
                            - $ref: '#/components/schemas/PublicUserSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user created
                  user:
                    UserSchema
        400:
          description: username or email is already taken
        403:
          description: user already logged in
      security: []
    """

    method_decorators = [jwt_required(optional=True)]

    def get(self):
        # retrieve multiple users' details

        # decide which query and schema to use
        query = User.query
        schema = None
        if current_user and current_user.role == User.Role.Admin:
            # user is an admin
            schema = UserSchema(many=True)
        else:
            # user is not logged in or not an admin
            query = query.filter_by(verified=True)
            schema = PublicUserSchema(many=True)

        return paginate(query, schema), 200

    def post(self):
        # creating a new account
        if current_user and current_user.role != User.Role.Admin:
            return {"msg": "user already logged in"}, 403

        schema = UserSchema()
        user = schema.load(request.json)

        if User.query.filter_by(email=user.email).first():
            return {"msg": "email is already taken"}, 400

        if User.query.filter_by(username=user.username).first():
            return {"msg": "username is already taken"}, 400

        db.session.add(user)
        db.session.commit()

        return {"msg": "user created", "user": schema.dump(user)}, 201


class UserCacheListResource(Resource):
    """Multiple objects resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: username
          schema:
            type: string
        - in: query
          name: order_by
          schema:
            type: string
          required: false
          description: field to order items by
        - in: query
          name: desc
          schema:
            type: boolean
          allowEmptyValue: true
          required: false
          description: order results descending
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
                          oneOf:
                            - $ref: '#/components/schemas/CacheSchema'
                            - $ref: '#/components/schemas/PublicCacheSchema'
        404:
          description: user not found
      security: []
    """

    method_decorators = [jwt_required(optional=True)]

    def get(self, username: str):
        # retrieve user's owned caches

        # find user
        user = User.query.filter_by(username=username, deleted=False).first_or_404()

        # decide which schema to use
        query = Cache.query.filter_by(owner=user, deleted=False)
        schema = None
        if current_user and (
            username == current_user.username or current_user.role == User.Role.Admin
        ):
            # owner or admin
            schema = CacheSchema(many=True)
        else:
            # default user
            schema = PublicCacheSchema(many=True)

        return paginate(query, schema), 200


class UserCacheVisitListResource(Resource):
    """Multiple objects resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: username
          schema:
            type: string
        - in: query
          name: order_by
          schema:
            type: string
          required: false
          description: field to order items by
        - in: query
          name: desc
          schema:
            type: boolean
          allowEmptyValue: true
          required: false
          description: order results descending
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
                          $ref: '#/components/schemas/CacheVisitSchema'
        404:
          description: user not found
    """

    method_decorators = [jwt_required()]

    def get(self, username: str):
        # retrieve user's cache visits

        # find user
        user = User.query.filter_by(username=username).first_or_404()

        query = CacheVisit.query.filter_by(user=user)
        schema = CacheVisitSchema(many=True)

        return paginate(query, schema), 200


class UserCacheCommentListResource(Resource):
    """Multiple objects resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: username
          schema:
            type: string
        - in: query
          name: order_by
          schema:
            type: string
          required: false
          description: field to order items by
        - in: query
          name: desc
          schema:
            type: boolean
          allowEmptyValue: true
          required: false
          description: order results descending
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
                          $ref: '#/components/schemas/CacheCommentSchema'
        404:
          description: user not found
      security: []
    """

    method_decorators = [jwt_required(optional=True)]

    def get(self, username: str):
        # retrieve user's cache comments

        # find user
        user = User.query.filter_by(username=username).first_or_404()

        query = CacheComment.query.filter_by(author=user, deleted=False)
        schema = CacheCommentSchema(many=True)

        return paginate(query, schema), 200
