from everycache_api.extensions import db, ma
from everycache_api.models import CacheVisit


class CacheVisitSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Integer(attribute="id_", dump_only=True)
    cache_id = ma.Integer(dump_only=True)
    user_username = ma.String(attribute="user.username", dump_only=True)
    visited_on = ma.DateTime(dump_only=True)

    class Meta:
        model = CacheVisit
        sqla_session = db.session
        load_instance = True
        ordered = True
        exclude = ("id_", "deleted", "user_id")
