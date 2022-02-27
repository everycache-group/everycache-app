from marshmallow import post_dump, validate

from everycache_api.extensions import ma
from everycache_api.models import Cache

from .base import BaseSchema
from .user import UserPublicSchema


class CacheSchema(BaseSchema):
    """Read-write schema used by logged-in users"""

    created_on = ma.DateTime(dump_only=True)
    lon = ma.Float(validate=validate.Range(-180.0, 180.0))
    lat = ma.Float(validate=validate.Range(-90.0, 90.0))
    name = ma.String(validate=validate.Length(min=5), required=True)
    description = ma.String(
        validate=validate.Length(min=10), required=False, default=""
    )
    rating = ma.Float(dump_only=True)
    owner = ma.Nested(UserPublicSchema, dump_only=True)
    visited = ma.Function(
        lambda cache, context: any(
            visit.user == context["current_user"] for visit in cache.visits
        ),
        dump_only=True,
    )

    @post_dump
    def fix_null_rating(self, data, many, **kwargs):
        if "rating" in self.fields and "rating" not in self.exclude:
            if data.get("rating") is None:
                data["rating"] = 0.0

        return data

    class Meta(BaseSchema.Meta):
        model = Cache


class CachePublicSchema(CacheSchema):
    """Read-only schema used by guests and nested in other schemas"""

    class Meta(CacheSchema.Meta):
        exclude = CacheSchema.Meta.exclude + ["visited"]
