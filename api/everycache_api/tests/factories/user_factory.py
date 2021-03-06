import factory

from everycache_api.extensions import db
from everycache_api.models import User as UserModel


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserModel
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    id_ = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: f"testowy-{n}")
    email = factory.Sequence(lambda n: f"testowy-{n}@example.com")

    role = UserModel.Role.Default
    password = factory.Sequence(lambda n: f"testpass{n}")
    deleted = False
    verified = True


class AdminFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserModel
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    username = "testowy_admin"
    email = "testowy_admin@example.com"
    role = UserModel.Role.Admin
    password = "testpassadmin"
    deleted = False
    verified = True
