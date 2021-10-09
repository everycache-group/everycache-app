from string import ascii_letters, digits

from everycache_api.extensions import db, ma
from everycache_api.models import User
from marshmallow import validate, validates
from marshmallow.exceptions import ValidationError
from marshmallow_enum import EnumField


class UserSchema(ma.SQLAlchemyAutoSchema):
    role = EnumField(User.Role)
    password = ma.String(load_only=True, required=True,
                         validate=validate.Length(8, 255))
    deleted = ma.Boolean(dump_only=True)

    @validates("username")
    def validate_username(self, value):
        def _validate_username_three_letters(value):
            if sum((value.count(let) for let in ascii_letters if let in value)) < 3:
                raise ValidationError(
                    "Must contain at least three letters.")

        return validate.And(
            validate.ContainsOnly(
                ascii_letters + "_" + digits,
                error="Must consist only of letters, digits and '_'."),
            validate.Length(5, 255),
            _validate_username_three_letters)(value)

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

    role = EnumField(User.Role)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        ordered = True
        fields = ("deleted", "role", "username")  # whitelist
