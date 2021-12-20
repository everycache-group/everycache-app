from flask import Blueprint, current_app, jsonify
from flask_restful import Api as BaseApi
from marshmallow.exceptions import ValidationError

from everycache_api.api.resources import (
    CacheCommentListResource,
    CacheCommentResource,
    CacheListResource,
    CacheResource,
    CacheVisitListResource,
    CacheVisitResource,
    UserCacheCommentListResource,
    UserCacheListResource,
    UserCacheVisitListResource,
    UserListResource,
    UserResource,
)
from everycache_api.api.schemas import (
    CacheCommentSchema,
    CacheSchema,
    CacheVisitSchema,
    PublicCacheSchema,
    PublicUserSchema,
    UserSchema,
)
from everycache_api.extensions import apispec

handled_exceptions = [ValidationError]


class Api(BaseApi):
    def error_router(self, original_handler, e):
        if type(e) in handled_exceptions:
            # pass exception through flask_restful to blueprint/app error handler
            return original_handler(e)

        return super().error_router(original_handler, e)


blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint)

resources = [
    (UserListResource, "/users", "users_list"),
    (UserResource, "/users/<string:user_id>", "user_by_username"),
    (UserCacheListResource, "/users/<string:user_id>/caches", "user_caches_list"),
    (UserCacheVisitListResource, "/users/<string:user_id>/visits", "user_visits_list"),
    (
        UserCacheCommentListResource,
        "/users/<string:user_id>/comments",
        "user_comments_list",
    ),
    (CacheListResource, "/caches", "caches_list"),
    (CacheResource, "/caches/<string:cache_id>", "cache_by_id"),
    (CacheVisitListResource, "/caches/<string:cache_id>/visits", "cache_visits_list"),
    (
        CacheCommentListResource,
        "/caches/<string:cache_id>/comments",
        "cache_comments_list",
    ),
    (CacheVisitResource, "/cache_visits/<string:cache_visit_id>", "cache_visit_by_id"),
    (
        CacheCommentResource,
        "/cache_comments/<string:cache_comment_id>",
        "cache_comment_by_id",
    ),
]

for resource, route, endpoint in resources:
    api.add_resource(resource, route, endpoint=endpoint)


@blueprint.before_app_first_request
def register_views():
    # apispec.spec.components.schema("CacheSchema", schema=CacheSchema)
    apispec.spec.components.schema("PublicCacheSchema", schema=PublicCacheSchema)
    apispec.spec.path(view=CacheResource, app=current_app)
    apispec.spec.path(view=CacheListResource, app=current_app)
    apispec.spec.path(view=CacheVisitListResource, app=current_app)
    apispec.spec.path(view=CacheCommentListResource, app=current_app)

    # apispec.spec.components.schema("CacheVisitSchema", schema=CacheVisitSchema)
    apispec.spec.path(view=CacheVisitResource, app=current_app)

    # apispec.spec.components.schema("CacheCommentSchema", schema=CacheCommentSchema)
    apispec.spec.path(view=CacheCommentResource, app=current_app)

    # apispec.spec.components.schema("UserSchema", schema=UserSchema)
    # apispec.spec.components.schema("PublicUserSchema", schema=PublicUserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserListResource, app=current_app)
    apispec.spec.path(view=UserCacheListResource, app=current_app)
    apispec.spec.path(view=UserCacheVisitListResource, app=current_app)
    apispec.spec.path(view=UserCacheCommentListResource, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
