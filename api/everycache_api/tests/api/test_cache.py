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


class TestCachePut:

    @pytest.fixture()
    def _put_data_dict(self):
        return {
            "lon": 2.3,
            "lat": 4.3,
            "name": "new_cache_name"
        }

    @pytest.fixture()
    def _put_data(self, _put_data_dict):
        return json.dumps(_put_data_dict)

    def _send_put_request(self, client, put_data, headers, cache_id):
        return client.put(
            f"/api/caches/{cache_id}",
            headers=headers,
            content_type="application/json",
            data=put_data)

    def test_put_unauthorized(self, client, _put_data):
        cache = CacheFactory()
        response = self._send_put_request(client, _put_data, {}, cache.id_)

        assert response.status_code == 401

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put_cache_not_found(self, logged_in_user_role, _put_data, client,
                                 logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(client, _put_data, headers, 2)

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put_cache_deleted(self, logged_in_user_role, _put_data, client,
                               logged_in_user):
        user, *_ = logged_in_user
        cache = CacheFactory(deleted=True, owner=user)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(client, _put_data, headers, cache.id_)
        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put_own_cache(self, logged_in_user_role, _put_data_dict, client,
                           logged_in_user):
        user, *_ = logged_in_user
        cache = CacheFactory(owner=user)

        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(
            client, json.dumps(_put_data_dict), headers, cache.id_)

        assert response.status_code == 200
        for key, value in _put_data_dict.items():
            assert type(value)(getattr(cache, key)) == value

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put_own_cache_by_deleted_user(self, logged_in_user_role, _put_data_dict,
                                           client, logged_in_user):
        user, *_ = logged_in_user
        user.deleted = True
        cache = CacheFactory(owner=user)

        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(
            client, json.dumps(_put_data_dict), headers, cache.id_)

        assert response.status_code == 403
        for key, value in _put_data_dict.items():
            assert type(value)(getattr(cache, key)) != value

    def test_put_other_users_cache(self, client, _put_data, logged_in_user):
        cache = CacheFactory()
        init_name = cache.name
        headers = get_headers_for_user(logged_in_user, User.Role.Default)
        response = self._send_put_request(
            client, _put_data, headers, cache.id_)

        assert response.status_code == 403
        assert cache.name == init_name

    def test_put_other_users_cache_by_admin(self, client, _put_data, logged_in_user):
        cache = CacheFactory()
        init_name = cache.name
        headers = get_headers_for_user(logged_in_user, User.Role.Admin)
        response = self._send_put_request(
            client, _put_data, headers, cache.id_)

        assert response.status_code == 200
        assert cache.name != init_name


class TestCacheDelete:

    def test_delete_unauthorized(self, client):
        cache = CacheFactory()
        response = client.delete(f"/api/caches/{cache.id_}")

        assert response.status_code == 401

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_delete_cache_not_found(self, logged_in_user_role, client, logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.delete("/api/caches/2", headers=headers)
        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_delete_cache_deleted(self, logged_in_user_role, client, logged_in_user):
        cache = CacheFactory(deleted=True)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.delete(f"/api/caches/{cache.id_}", headers=headers)
        assert response.status_code == 404

    def test_delete_other_users_cache(self, client, logged_in_user):
        cache = CacheFactory()
        headers = get_headers_for_user(logged_in_user, User.Role.Default)

        response = client.delete(f"/api/caches/{cache.id_}", headers=headers)

        assert response.status_code == 403
        assert cache.deleted is False

    def test_delete_other_users_cache_by_admin(self, client, logged_in_user):
        cache = CacheFactory()
        headers = get_headers_for_user(logged_in_user, User.Role.Admin)

        response = client.delete(f"/api/caches/{cache.id_}", headers=headers)

        assert response.status_code == 200
        assert cache.deleted is True

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_delete_own_cache(self, logged_in_user_role, client, logged_in_user):
        user, *_ = logged_in_user
        cache = CacheFactory(owner=user)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.delete(f"/api/caches/{cache.id_}", headers=headers)

        assert response.status_code == 200
        assert cache.deleted is True

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_delete_own_cache_by_deleted_user(self, logged_in_user_role,
                                              client, logged_in_user):
        user, *_ = logged_in_user
        user.deleted = True
        cache = CacheFactory(owner=user)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.delete(f"/api/caches/{cache.id_}", headers=headers)

        assert response.status_code == 403
        assert cache.deleted is False
