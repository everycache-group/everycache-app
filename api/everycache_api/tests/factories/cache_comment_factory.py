import factory
import factory.fuzzy

from everycache_api.extensions import db
from everycache_api.models import CacheComment as CacheCommentModel
from everycache_api.tests.factories.cache_factory import CacheFactory
from everycache_api.tests.factories.user_factory import UserFactory


class CacheCommentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = CacheCommentModel
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    deleted = False
    id_ = factory.Sequence(lambda n: n)

    text = factory.Faker("text")

    author = factory.SubFactory(UserFactory)
    cache = factory.SubFactory(CacheFactory)
