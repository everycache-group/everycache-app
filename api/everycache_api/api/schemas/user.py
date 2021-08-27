from everycache_api.extensions import db, ma
from everycache_api.models import User


# general user resource schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    email = ma.String(load_only=True, required=True)
    password = ma.String(load_only=True, required=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        fields = ('username', 'password', 'email')


class UserSchemaForAdmins(ma.SQLAlchemyAutoSchema):
    password = ma.String(load_only=True, required=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ('_password',)

# user details resource schema, this one should require logging in
# class UserDetailsSchema(ma.SQLAlchemyAutoSchema):
#     active = ma.Boolean(dump_only=True)

#     class Meta:
#         model = User
#         sqla_session = db.session
#         load_instance = True
#         fields = ("username", "active")


# # user details for currently logged in user (uses jwt to specify the user)
# class CurrentUserDetailsSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = User
#         sqla_session = db.session
#         load_instance = True
#         fields = ("username", "email", "verified", "active")
