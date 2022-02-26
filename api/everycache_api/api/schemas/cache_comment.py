from everycache_api.extensions import ma
from everycache_api.models import CacheComment

from .base import BaseSchema
from .cache import CachePublicSchema
from .user import UserPublicSchema


class CacheCommentSchema(BaseSchema):
    cache_id = ma.Pluck(
        CachePublicSchema, field_name="id", attribute="cache", dump_only=True
    )
    author = ma.Nested(UserPublicSchema, dump_only=True)
    created_on = ma.DateTime(dump_only=True)

    class Meta(BaseSchema.Meta):
        model = CacheComment
        exclude = BaseSchema.Meta.exclude + ["user_id"]
