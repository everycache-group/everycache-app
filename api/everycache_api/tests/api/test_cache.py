import json

import pytest

from everycache_api.api.schemas.cache import CacheSchema, PublicCacheSchema
from everycache_api.models import Cache, User
from everycache_api.tests.factories.cache_factory import CacheFactory
from everycache_api.tests.helpers import get_headers_for_user


class TestCacheGet:

    @pytest.mark.parametrize("logged_in_user_role", (None, *list(User.Role)))
    def test_get_cache_not_found(self, logged_in_user_role, client, logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.get("/api/caches/cache_id", headers=headers)

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", (None, *list(User.Role)))
    def test_get_cache_deleted(self, logged_in_user_role, client, logged_in_user):
        cache = CacheFactory(deleted=True)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.get(f"/api/caches/{cache.id_}", headers=headers)

        assert response.status_code == 404

    @pytest.mark.parametrize("is_user_logged_in", (True, False))
    def test_get_cache_other_user_public(self, is_user_logged_in, client,
                                         logged_in_user):
        cache = CacheFactory()
        role = User.Role.Default if is_user_logged_in else None
        headers = get_headers_for_user(logged_in_user, role)

        response = client.get(f"/api/caches/{cache.id_}", headers=headers)

        cache = Cache.query.filter_by(id_=cache.id_).first()
        cache_deserailized = json.loads(PublicCacheSchema().dumps(cache))
        assert response.status_code == 200
        assert response.json["cache"] == cache_deserailized

    def test_get_other_user_cache_by_admin(self, client, logged_in_user):
        cache = CacheFactory()
        headers = get_headers_for_user(logged_in_user, User.Role.Admin)

        response = client.get(f"/api/caches/{cache.id_}", headers=headers)

        assert response.status_code == 200
        cache = Cache.query.filter_by(id_=cache.id_).first()
        cache_deserailized = json.loads(CacheSchema().dumps(cache))

        assert response.json["cache"] == cache_deserailized

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_get_own_cache(self, logged_in_user_role, client, logged_in_user):
        user, *_ = logged_in_user
        cache = CacheFactory(owner=user)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.get(f"/api/caches/{cache.id_}", headers=headers)

        assert response.status_code == 200
        cache = Cache.query.filter_by(id_=cache.id_).first()
        cache_deserailized = json.loads(CacheSchema().dumps(cache))

        assert response.json["cache"] == cache_deserailized
