from flask import Blueprint
from flask import current_app as app
from flask import jsonify
from flask_restful import Api
from marshmallow import ValidationError

from everycache_api.api.resources import UserList, UserResource
from everycache_api.api.schemas import UserSchema
from everycache_api.extensions import apispec

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=app)
    apispec.spec.path(view=UserList, app=app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
