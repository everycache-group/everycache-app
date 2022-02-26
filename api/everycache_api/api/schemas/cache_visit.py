from marshmallow import validate

from everycache_api.extensions import ma
from everycache_api.models import CacheVisit

from .base import BaseSchema
from .cache import CachePublicSchema
from .user import UserPublicSchema


class CacheVisitSchema(BaseSchema):
    cache_id = ma.Pluck(
        CachePublicSchema, field_name="id", attribute="cache", dump_only=True
    )
    user = ma.Nested(UserPublicSchema, dump_only=True)
    visited_on = ma.DateTime(dump_only=True)
    rating = ma.Integer(validate=validate.Range(0, 5))

    class Meta(BaseSchema.Meta):
        model = CacheVisit
        exclude = BaseSchema.Meta.exclude + ["user_id"]
