from flask import abort, request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from everycache_api.api.schemas import (
    CacheCommentSchema,
    CacheSchema,
    CacheVisitSchema,
    UserAdminSchema,
    UserPublicSchema,
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
          name: user_id
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
                      - UserPublicSchema
        404:
          description: user not found
      security: []
    put:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
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
                  message:
                    type: string
                    example: User updated.
                  user:
                    UserUpdateSchema
        403:
          description: forbidden
        404:
          description: user not found
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: User deleted.
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

    def get(self, user_id: str):
        # find user
        user = User.query_ext_id(user_id).filter_by(deleted=False).first_or_404()

        # decide which schema to use
        schema = None
        if current_user and (
            current_user.ext_id == user_id or current_user.role == User.Role.Admin
        ):
            # user is querying own account info or is an admin
            schema = UserSchema()
        else:
            # user is not logged in or is querying other user's account info
            schema = UserPublicSchema()

        # return user details
        return {"user": schema.dump(user)}, 200

    def put(self, user_id: str):
        # ensure current_user is authorized
        if current_user.ext_id != user_id and current_user.role != User.Role.Admin:
            abort(403, "Unauthorized to modify other users.")

        # find user
        user = User.query_ext_id(user_id).filter_by(deleted=False).first_or_404()

        # update and return user details
        errors = {}

        if user == current_user:
            # user changing own data; ensure current password is correct
            current_password = request.json.pop("current_password", "")

            if not len(current_password):
                errors["current_password"] = ["Current password is required for updating user data."]

            elif not user.verify_password(current_password):
                errors["current_password"] = ["Current password is incorrect."]


        if current_user.role == User.Role.Admin:
            # admin changing other user's data
            schema = UserAdminSchema(partial=True)
        else:
            schema = UserSchema(partial=True)

        # ensure new email and/or new username are not already taken
        email = request.json.get("email")
        username = request.json.get("username")

        if (
            email
            and User.query.filter(User.email == email, User.id_ != user.id_).first()
        ):
            errors["email"] = ["Email is already taken."]

        if (
            username
            and User.query.filter(
                User.username == username, User.id_ != user.id_
            ).first()
        ):
            errors["username"] = ["Username is already taken."]

        if errors:
            raise ValidationError(errors)

        # update and return user data
        user = schema.load(request.json, instance=user, partial=True)

        db.session.commit()

        return {"message": "User updated.", "user": schema.dump(user)}, 200

    def delete(self, user_id: str):
        # ensure current_user is authorized
        if current_user.ext_id != user_id and current_user.role != User.Role.Admin:
            abort(403, "Unauthorized to delete other users.")

        # find user
        user = User.query_ext_id(user_id).filter_by(deleted=False).first_or_404()

        # mark user as deleted
        user.deleted = True
        db.session.commit()

        # revoke any tokens for deleted user
        revoke_all_user_tokens(user)

        return {"message": "User deleted."}, 200


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
                            - $ref: '#/components/schemas/UserPublicSchema'
                            - $ref: '#/components/schemas/UserSchema'
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
                  message:
                    type: string
                    example: User created.
                  user:
                    UserSchema
        400:
          description: bad request
        403:
          description: user already logged in
      security: []
    """

    method_decorators = [jwt_required(optional=True)]

    def get(self):
        # retrieve multiple users' details
        query = User.query.filter_by(deleted=False)

        # decide which schema to use
        schema = None
        if current_user and current_user.role == User.Role.Admin:
            # user is an admin
            schema = UserSchema(many=True)
        else:
            # user is not logged in or not an admin
            query = query.filter_by(verified=True)
            schema = UserPublicSchema(many=True)

        return paginate(query, schema), 200

    def post(self):
        # creating a new account
        schema = None

        if current_user:
            if current_user.role == User.Role.Admin:
                schema = UserAdminSchema()
            else:
                abort(403, "User already logged in.")
        else:
            schema = UserSchema()

        user = schema.load(request.json)

        errors = {}

        if User.query.filter_by(email=user.email).first():
            errors["email"] = ["Email is already taken."]

        if User.query.filter_by(username=user.username).first():
            errors["username"] = ["Username is already taken."]

        if errors:
            raise ValidationError(errors)

        db.session.add(user)
        db.session.commit()

        return {"message": "User created.", "user": schema.dump(user)}, 201


class UserCacheListResource(Resource):
    """Multiple objects resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
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
                            - $ref: '#/components/schemas/CachePublicSchema'
        404:
          description: user not found
      security: []
    """

    method_decorators = [jwt_required(optional=True)]

    def get(self, user_id: str):
        # retrieve user's owned caches

        # find user
        user = User.query_ext_id(user_id).filter_by(deleted=False).first_or_404()

        # decide which schema to use
        query = Cache.query.filter_by(owner=user, deleted=False)
        schema = None
        if current_user:
            # logged in user
            if current_user == user:
                schema = CacheSchema(many=True, exclude=["visited"])
            else:
                schema = CacheSchema(many=True)
                schema.context = {"current_user": current_user}
        else:
            # guest user
            schema = UserPublicSchema(many=True)

        return paginate(query, schema), 200


class UserCacheVisitListResource(Resource):
    """Multiple objects resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
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
      security: []
    """

    method_decorators = [jwt_required()]

    def get(self, user_id: str):
        # retrieve user's cache visits

        # find user
        user = User.query_ext_id(user_id).first_or_404()

        query = CacheVisit.query.filter_by(user=user, deleted=False).filter(
            CacheVisit.cache.has(deleted=False)
        )
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
          name: user_id
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

    def get(self, user_id: str):
        # retrieve user's cache comments

        # find user
        user = User.query_ext_id(user_id).filter_by(deleted=False).first_or_404()

        query = CacheComment.query.filter_by(author=user, deleted=False).filter(
            CacheComment.cache.has(deleted=False)
        )
        schema = CacheCommentSchema(many=True)

        return paginate(query, schema), 200
