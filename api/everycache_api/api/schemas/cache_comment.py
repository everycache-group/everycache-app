from everycache_api.extensions import db, ma
from everycache_api.models import CacheComment

from .cache import PublicCacheSchema
from .user import NestedUserSchema


class CacheCommentSchema(ma.SQLAlchemyAutoSchema):
    id = ma.String(attribute="ext_id", dump_only=True)
    cache_id = ma.Pluck(
        PublicCacheSchema, field_name="id", attribute="cache", dump_only=True
    )
    author = ma.Nested(NestedUserSchema, dump_only=True)
    created_on = ma.DateTime(dump_only=True)

    class Meta:
        model = CacheComment
        sqla_session = db.session
        load_instance = True
        ordered = True
        exlude = ("id_", "deleted", "user_id")
