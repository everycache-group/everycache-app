from everycache_api.extensions import db, ma
from everycache_api.models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        # exclude = ("__password",)
