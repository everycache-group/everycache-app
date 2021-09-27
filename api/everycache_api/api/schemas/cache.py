from everycache_api.extensions import db, ma
from everycache_api.models import Cache

from .user import PublicUserSchema, UserSchema


class CacheSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Integer(attribute="id_", dump_only=True)
    created_on = ma.DateTime(dump_only=True)
    lon = ma.Float()
    lat = ma.Float()
    owner_username = ma.Pluck(
        UserSchema, field_name="username", attribute="owner", dump_only=True
    )

    class Meta:
        model = Cache
        sqla_session = db.session
        load_instance = True
        ordered = True
        exclude = ("id_", "deleted")


class PublicCacheSchema(ma.SQLAlchemyAutoSchema):
    """Read-only schema"""

    id = ma.Integer(attribute="id_", dump_only=True)
    created_on = ma.DateTime(dump_only=True)
    lon = ma.Float()
    lat = ma.Float()
    owner_username = ma.Pluck(
        PublicUserSchema, field_name="username", attribute="owner", dump_only=True
    )

    class Meta:
        model = Cache
        sqla_session = db.session
        load_instance = True
        ordered = True
        exclude = ("id_", "deleted")
