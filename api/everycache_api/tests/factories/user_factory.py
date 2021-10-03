import factory
from everycache_api.models import User as UserModel
from everycache_api.extensions import db


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserModel
        sqlalchemy_session = db.session

    username = "testowy"
    email = "testowy@example.com"
    role = UserModel.Role.Default
    password = "testpass"
