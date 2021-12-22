import pytest
from fakeredis import FakeRedis
import everycache_api.extensions


@pytest.fixture(scope="function", autouse=True)
def redis_client():
    redis_client = FakeRedis()
    everycache_api.extensions.redis_client = redis_client
    everycache_api.auth.helpers.redis_client = redis_client
    everycache_api.auth.storage_helper.redis_client = redis_client

    yield redis_client

    everycache_api.extensions.redis_client = False
    everycache_api.auth.helpers.redis_client = False
    everycache_api.auth.storage_helper.redis_client = False
