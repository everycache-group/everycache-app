from marshmallow import validate

from everycache_api.extensions import db, ma
from everycache_api.models import CacheVisit

from .cache import PublicCacheSchema
from .user import NestedUserSchema


class CacheVisitSchema(ma.SQLAlchemyAutoSchema):
    id = ma.String(attribute="ext_id", dump_only=True)
    cache_id = ma.Pluck(
        PublicCacheSchema, field_name="id", attribute="cache", dump_only=True
    )
    user = ma.Nested(NestedUserSchema, dump_only=True)
    visited_on = ma.DateTime(dump_only=True)
    rating = ma.Float(validate=validate.Range(0.5, 5.0))

    class Meta:
        model = CacheVisit
        sqla_session = db.session
        load_instance = True
        ordered = True
        exclude = ("id_", "deleted", "user_id")
