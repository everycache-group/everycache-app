from everycache_api.extensions import db, ma
from everycache_api.models import CacheComment


class CacheCommentSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Integer(attribute="id_", dump_only=True)
    cache_id = ma.Integer(dump_only=True)
    user_username = ma.String(attribute="user.username", dump_only=True)
    created_on = ma.DateTime(dump_only=True)

    class Meta:
        model = CacheComment
        sqla_session = db.session
        load_instance = True
        ordered = True
        exlude = ("id_", "deleted", "user_id")
