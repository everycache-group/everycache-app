import factory
from everycache_api.models import User as UserModel
from everycache_api.extensions import db


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserModel
        sqlalchemy_session = db.session

    id_ = factory.Sequence(lambda n: f"{n}")
    username = factory.Sequence(lambda n: f"testowy-{n}")
    email = factory.Sequence(lambda n: f"testowy-{n}@example.com")

    role = UserModel.Role.Default
    password = factory.Sequence(lambda n: f"testpass{n}")


class AdminFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserModel
        sqlalchemy_session = db.session

    username = "testowy_admin"
    email = "testowy_admin@example.com"
    role = UserModel.Role.Admin
    password = "testpassadmin"
