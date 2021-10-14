from everycache_api.extensions import db, ma
from everycache_api.models import Cache
from marshmallow import validate

from .user import NestedUserSchema


class CacheSchema(ma.SQLAlchemyAutoSchema):
    id = ma.String(attribute="ext_id", dump_only=True)
    created_on = ma.DateTime(dump_only=True)
    lon = ma.Float(validate=validate.Range(-180.0, 180.0))
    lat = ma.Float(validate=validate.Range(-90.0, 90.0))
    owner = ma.Nested(NestedUserSchema, dump_only=True)
    name = ma.String(validate=validate.Length(min=5), required=False)
    description = ma.String(validate=validate.Length(min=5), required=False)

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
