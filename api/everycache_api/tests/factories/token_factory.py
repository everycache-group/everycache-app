import datetime
from datetime import datetime, timezone

import factory
from factory.fuzzy import FuzzyDateTime

from everycache_api.extensions import db
from everycache_api.models import Token as TokenModel
from everycache_api.tests.factories.user_factory import UserFactory


class TokenFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = TokenModel
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    jti = factory.Sequence(lambda n: f"test_jti-{n}")
    token_type = "refresh"
    revoked = False
    user = factory.SubFactory(UserFactory)
    expires = FuzzyDateTime(
        datetime.now(timezone.utc),
        datetime(2169, 1, 1, tzinfo=timezone.utc)
    )
