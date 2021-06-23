from everycache_api.extensions import db, ma
from everycache_api.models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)
    
    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("_password",)
