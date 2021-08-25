from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from everycache_api.api.resources import (
    CacheList,
    CacheResource,
    ProfileResource,
    UserList,
    UserResource,
)
from everycache_api.api.schemas import CacheSchema, ProfileSchema, UserSchema
from everycache_api.extensions import apispec

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint)

api.add_resource(UserList, "/users", endpoint="users_list")
api.add_resource(UserResource, "/users/<string:username>", endpoint="user_by_username")

api.add_resource(ProfileResource, "/profile", endpoint="profile")

api.add_resource(CacheList, "/caches", endpoint="caches_list")
api.add_resource(CacheResource, "/caches/<int:id>", endpoint="cache_by_id")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)

    apispec.spec.components.schema("ProfileSchema", schema=ProfileSchema)
    apispec.spec.path(view=ProfileResource, app=current_app)

    apispec.spec.components.schema("CacheSchema", schema=CacheSchema)
    apispec.spec.path(view=CacheResource, app=current_app)
    apispec.spec.path(view=CacheList, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
