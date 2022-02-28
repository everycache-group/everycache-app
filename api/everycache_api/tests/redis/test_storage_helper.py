from datetime import datetime, timedelta

from everycache_api.auth.storage_helper import load_tokens_from_database_to_storage
from everycache_api.tests.factories.token_factory import TokenFactory


def test_db_to_storage(redis_client):
    token_1 = TokenFactory()
    TokenFactory(revoked=True)
    TokenFactory(expires=datetime.utcnow() - timedelta(seconds=50))

    load_tokens_from_database_to_storage()

    keys = redis_client.keys()
    assert len(keys) == 1
    assert token_1.jti in next(iter(keys)).decode()
