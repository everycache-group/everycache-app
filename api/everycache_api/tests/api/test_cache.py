import json

import pytest

from everycache_api.api.schemas.cache import CacheSchema, PublicCacheSchema
from everycache_api.models import Cache, User
from everycache_api.tests.factories.cache_factory import CacheFactory
from everycache_api.tests.helpers import get_auth_header, get_headers_for_user


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
        cache_deserialized = json.loads(PublicCacheSchema().dumps(cache))
        assert response.status_code == 200
        assert response.json["cache"] == cache_deserialized

    def test_get_other_user_cache_by_admin(self, client, logged_in_user):
        cache = CacheFactory()
        headers = get_headers_for_user(logged_in_user, User.Role.Admin)

        response = client.get(f"/api/caches/{cache.id_}", headers=headers)

        assert response.status_code == 200
        cache = Cache.query.filter_by(id_=cache.id_).first()
        cache_deserialized = json.loads(CacheSchema().dumps(cache))

        assert response.json["cache"] == cache_deserialized

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_get_own_cache(self, logged_in_user_role, client, logged_in_user):
        user, *_ = logged_in_user
        cache = CacheFactory(owner=user)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.get(f"/api/caches/{cache.id_}", headers=headers)

        assert response.status_code == 200
        cache = Cache.query.filter_by(id_=cache.id_).first()
        cache_deserialized = json.loads(CacheSchema().dumps(cache))

        assert response.json["cache"] == cache_deserialized


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


class TestCacheListGet:

    @pytest.mark.parametrize("is_user_logged_in", (False, True))
    def test_get_public_list(self, is_user_logged_in, client, logged_in_user):
        user, access_token, _ = logged_in_user
        cache = CacheFactory()
        for _ in range(5):
            CacheFactory()

        headers = {}
        if is_user_logged_in:
            headers = get_auth_header(access_token)

        response = client.get("/api/caches", headers=headers)

        caches = Cache.query.all()
        caches_expected = json.loads(PublicCacheSchema().dumps(caches, many=True))
        assert cache in caches
        assert response.json["results"] == caches_expected
        assert response.status_code == 200

    def test_get_admin_list(self, client, logged_in_user):
        for _ in range(5):
            CacheFactory()

        headers = get_headers_for_user(logged_in_user, User.Role.Admin)
        response = client.get("/api/caches", headers=headers)

        expected_caches = json.loads(
            CacheSchema().dumps(Cache.query.all(), many=True))

        assert response.json["results"] == expected_caches
        assert response.status_code == 200

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_get_deleted_cache_hidden(self, logged_in_user_role, client,
                                      logged_in_user):
        cache = CacheFactory()
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.get("/api/caches", headers=headers)
        assert len(response.json["results"]) == 1

        cache.deleted = True

        response = client.get("/api/caches", headers=headers)
        assert len(response.json["results"]) == 0


class TestCacheListPost:

    @pytest.fixture()
    def _post_data_dict(self):
        return {
            "lon": 2.3,
            "lat": 4.3,
            "name": "new_cache_name"
        }

    @pytest.fixture()
    def _post_data(self, _post_data_dict):
        return json.dumps(_post_data_dict)

    def _send_post_request(self, client, post_data, headers):
        return client.post(
            "/api/caches",
            headers=headers,
            content_type="application/json",
            data=post_data)

    def test_post_unauthorized(self, client, _post_data):
        assert Cache.query.count() == 0
        response = self._send_post_request(client, _post_data, {})

        assert response.status_code == 401
        assert Cache.query.count() == 0

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_post_cache_created(self, logged_in_user_role, client, _post_data_dict,
                                logged_in_user):
        user, *_ = logged_in_user
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        _post_data = json.dumps(_post_data_dict)

        assert Cache.query.count() == 0
        response = self._send_post_request(client, _post_data, headers)

        assert response.status_code == 201
        assert Cache.query.count() == 1
        cache = Cache.query.first()
        for key, value in _post_data_dict.items():
            assert type(value)(getattr(cache, key)) == value
        assert cache.owner == user
