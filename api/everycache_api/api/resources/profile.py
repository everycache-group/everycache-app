from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from everycache_api.api.schemas import ProfileSchema
from everycache_api.models import User


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
        "get": jwt_required(),
        "put": jwt_required(),
    }

    def get(self):
        user_id = get_jwt_identity()

        schema = ProfileSchema()
        user = User.query.filter_by(id_=user_id).one_or_404()

        return {"user": schema.dump(user)}

    def post(self):
        """Creating a new account"""
        schema = ProfileSchema()

        user = schema.load(schema)
