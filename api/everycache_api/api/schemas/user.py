from marshmallow_enum import EnumField

from everycache_api.extensions import db, ma
from everycache_api.models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    role = EnumField(User.Role)
    password = ma.String(load_only=True, required=True)
    deleted = ma.Boolean(dump_only=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        ordered = True
        exclude = ("id_", "deleted", "_password")


class PublicUserSchema(ma.SQLAlchemyAutoSchema):
    """Read-only schema"""

    role = EnumField(User.Role)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        ordered = True
        fields = ("deleted", "role", "username")  # whitelist
