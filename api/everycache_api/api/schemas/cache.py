from everycache_api.extensions import db, ma
from everycache_api.models import Cache

from .user import NestedUserSchema


class CacheSchema(ma.SQLAlchemyAutoSchema):
    id = ma.String(attribute="ext_id", dump_only=True)
    created_on = ma.DateTime(dump_only=True)
    lon = ma.Float()
    lat = ma.Float()
    owner = ma.Nested(NestedUserSchema, dump_only=True)

    class Meta:
        model = Cache
        sqla_session = db.session
        load_instance = True
        ordered = True
        exclude = ("id_", "deleted")


class PublicCacheSchema(ma.SQLAlchemyAutoSchema):
    """Read-only schema"""

    id = ma.String(attribute="ext_id", dump_only=True)
    created_on = ma.DateTime(dump_only=True)
    lon = ma.Float()
    lat = ma.Float()
    owner = ma.Nested(NestedUserSchema, dump_only=True)

    class Meta:
        model = Cache
        sqla_session = db.session
        load_instance = True
        ordered = True
        exclude = ("id_", "deleted")
