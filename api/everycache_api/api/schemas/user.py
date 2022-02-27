from collections import Counter
from string import ascii_letters, digits, whitespace

from marshmallow import validate, validates
from marshmallow.exceptions import ValidationError
from marshmallow.fields import String
from marshmallow_enum import EnumField

from everycache_api.extensions import ma
from everycache_api.models import User

from .base import BaseSchema


class UserSchema(BaseSchema):
    """Read-write schema used by admins and users querying themselves"""

    username = ma.String(required=True)
    email = ma.String(required=True, validate=validate.Email())
    password = ma.String(
        load_only=True,
        validate=[
            validate.ContainsNoneOf(
                whitespace, error="Must not contain any whitespace"),
            validate.Length(8, 255)],
        required=True,
    )
    role = EnumField(User.Role, dump_only=True)
    verified = ma.Boolean(dump_only=True)

    @validates("username")
    def validate_username(self, value: str):
        def validate_first_letter(value: str):
            if value[0] not in ascii_letters:
                raise ValidationError("Must start with a letter.")

        def validate_three_letters(value: str):
            counter = Counter(value)

            if sum(counter.get(s, 0) for s in ascii_letters) < 3:
                raise ValidationError("Must contain at least three letters.")

        return validate.And(
            validate.Length(5, 255),
            validate_first_letter,
            validate.ContainsOnly(
                ascii_letters + "_" + digits,
                error="Must consist only of letters, digits and '_'.",
            ),
            validate_three_letters,
        )(value)

    class Meta(BaseSchema.Meta):
        model = User
        exclude = BaseSchema.Meta.exclude + ["_password"]


class UserUpdateSchema(UserSchema):
    """
    Schema used for updating current user's data; never actually loaded, but specifies
    current_password field for /api/users/<user_id> PUT endpoint in api specification
    """

    current_password: String = ma.String(load_only=True, required=True)


class UserPublicSchema(UserSchema):
    """Read-only schema used by guests and default users querying others"""

    class Meta(UserSchema.Meta):
        exclude = []
        fields = ["id", "username"]  # whitelist


class UserAdminSchema(UserSchema):
    """Read-write schema used by admins for changing other users' data"""

    role = EnumField(User.Role)
    verified = ma.Boolean()
