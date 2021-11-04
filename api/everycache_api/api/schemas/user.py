from string import ascii_letters, digits

from marshmallow import validate, validates
from marshmallow.exceptions import ValidationError
from marshmallow_enum import EnumField

from everycache_api.extensions import db, ma
from everycache_api.models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    id = ma.String(attribute="ext_id", dump_only=True)
    username = ma.String(required=False)
    email = ma.String(required=False)
    password = ma.String(
        load_only=True, required=True, validate=validate.Length(8, 255)
    )
    role = EnumField(User.Role)

    @validates("username")
    def validate_username(self, value):
        def _validate_username_three_letters(value):
            if sum((value.count(let) for let in ascii_letters if let in value)) < 3:
                raise ValidationError("Must contain at least three letters.")

        return validate.And(
            validate.ContainsOnly(
                ascii_letters + "_" + digits,
                error="Must consist only of letters, digits and '_'.",
            ),
            validate.Length(5, 255),
            _validate_username_three_letters,
        )(value)

    @validates("email")
    def validate_email(self, value):
        return validate.Email()(value)

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
