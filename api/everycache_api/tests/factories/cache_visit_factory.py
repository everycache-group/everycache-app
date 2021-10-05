
import factory
import factory.fuzzy

from everycache_api.extensions import db
from everycache_api.models import CacheVisit as CacheVisitModel
from everycache_api.tests.factories.cache_factory import CacheFactory
from everycache_api.tests.factories.user_factory import UserFactory


class CacheVisitFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = CacheVisitModel
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    deleted = False
    id_ = factory.Sequence(lambda n: n)
    user = factory.SubFactory(UserFactory)
    cache = factory.SubFactory(CacheFactory)
