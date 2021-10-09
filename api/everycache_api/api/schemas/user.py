from marshmallow_enum import EnumField

from everycache_api.extensions import db, ma
from everycache_api.models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    id = ma.String(attribute="ext_id", dump_only=True)
    username = ma.String(required=False)
    email = ma.String(required=False)
    password = ma.String(load_only=True, required=True)
    role = EnumField(User.Role)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        ordered = True
        exclude = ("id_", "deleted", "_password")


class PublicUserSchema(ma.SQLAlchemyAutoSchema):
    """Read-only schema"""

    id = ma.String(attribute="ext_id", dump_only=True)
    role = EnumField(User.Role)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        ordered = True
        fields = ("id", "role", "username")  # whitelist


class NestedUserSchema(ma.SQLAlchemyAutoSchema):
    """Used in other schemas"""

    id = ma.String(attribute="ext_id", dump_only=True)
    username = ma.String(dump_only=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        ordered = True
        fields = ("id", "username")  # whitelist
