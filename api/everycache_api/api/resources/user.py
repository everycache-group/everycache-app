from everycache_api.users.helpers import add_user
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource

from everycache_api.api.schemas import UserSchema
from everycache_api.api.schemas.user import UserSchemaForAdmins
from everycache_api.common.pagination import paginate
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
    method_decorators = [jwt_required()]

    def get(self, username: str):
        if not current_user or current_user.role != User.Role.admin:
            return {}, 403

        schema = UserSchemaForAdmins()
        user = User.query.filter_by(username=username).first_or_404()

        return {"user": schema.dump(user)}


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

    method_decorators = [jwt_required(optional=True)]

    def get(self):
        schema_type = UserSchema

        if current_user and current_user.role == User.Role.admin:
            schema_type = UserSchemaForAdmins

        schema = schema_type(many=True)
        query = User.query

        return paginate(query, schema)

    def post(self):
        if not current_user or current_user.role != User.Role.admin:
            return {}, 403

        schema = UserSchemaForAdmins()
        return add_user(schema)
