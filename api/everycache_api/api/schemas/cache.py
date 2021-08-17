from everycache_api.extensions import db, ma
from everycache_api.models import Cache, CacheComment, CacheVisit, User

from .user import UserSchema


# general cache resource schema
class CacheSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Integer(attribute="id_")
    lon = ma.Float()
    lat = ma.Float()
    owner_username = ma.String(attribute="owner.username")

    class Meta:
        model = Cache
        sqla_session = db.session
        load_instance = True
        exclude = ("id_",)


class CacheDetailsSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Integer(attribute="id_")

    class Meta:
        model = Cache
        sqla_session = db.session
        load_instance = True
        # fields = ("id_",)
        # exclude = ("owner_id",)
