from everycache_api.extensions import ma

from .user import UserSchema


class ProfileSchema(UserSchema):
    email = ma.Email()
