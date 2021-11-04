import factory
import factory.fuzzy

from everycache_api.extensions import db
from everycache_api.models import Cache as CacheModel
from everycache_api.tests.factories.user_factory import UserFactory


class CacheFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = CacheModel
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    deleted = False
    id_ = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"testowy-cache-{n}")
    lon = factory.fuzzy.FuzzyFloat(-180.0, 180.0, precision=4)
    lat = factory.fuzzy.FuzzyFloat(-180.0, 180.0, precision=4)
    owner = factory.SubFactory(UserFactory)
    description = factory.Sequence(lambda n: f"testowy-cache-opis-{n}")
