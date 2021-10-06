import json

import pytest

from everycache_api.api.schemas.cache_visit import CacheVisitSchema
from everycache_api.models import CacheVisit, User
from everycache_api.tests.factories.cache_visit_factory import CacheVisitFactory
from everycache_api.tests.helpers import get_headers_for_user


class TestCacheVisitGet:

    def test_get_cache_visit_not_found(self, client):
        response = client.get("/api/cache_visits/2")

        assert response.status_code == 404

    def test_get_cache_visit_deleted(self, client):
        cache_visit = CacheVisitFactory(deleted=True)

        response = client.get(f"/api/cache_visits/{cache_visit.id_}")

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", (None, *list(User.Role)))
    def test_get(self, logged_in_user_role, client, logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        cache_visit = CacheVisitFactory()

        response = client.get(f"/api/cache_visits/{cache_visit.id_}", headers=headers)

        assert CacheVisit.query.count() == 1
        db_visit = CacheVisit.query.first()
        expected_data = json.loads(CacheVisitSchema().dumps(db_visit))

        assert response.status_code == 200
        assert response.json["cache_visit"] == expected_data

    @pytest.mark.parametrize("attr_name", ("user", "cache"))
    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_get_related_object_deleted(self, attr_name, logged_in_user_role, client,
                                        logged_in_user):
        cache_visit = CacheVisitFactory()
        getattr(cache_visit, attr_name).deleted = True

        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.get(f"/api/cache_visits/{cache_visit.id_}", headers=headers)

        assert response.status_code == 404


class TestCacheVisitPut:

    @pytest.fixture()
    def _put_data_dict(self):
        return {
            "rating": 3,
        }

    @pytest.fixture()
    def _put_data(self, _put_data_dict):
        return json.dumps(_put_data_dict)

    def _send_put_request(self, client, cache_visit_id, headers, put_data):
        return client.put(
            f"/api/cache_visits/{cache_visit_id}",
            content_type="application/json",
            headers=headers,
            data=put_data)

    def test_put_unauthorized(self, client, _put_data):
        cache_visit = CacheVisitFactory()

        response = self._send_put_request(client, cache_visit.id_, {}, _put_data)

        assert response.status_code == 401

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put_cache_visit_not_found(self, logged_in_user_role, client, _put_data,
                                       logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(client, 2, headers, _put_data)

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put_cache_visit_deleted(self, logged_in_user_role, client, _put_data,
                                     logged_in_user):
        cache_visit = CacheVisitFactory(deleted=True)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(client, cache_visit.id_, headers, _put_data)

        assert response.status_code == 404

    def test_put_other_users_cache_visit(self, client, _put_data, logged_in_user):
        cache_visit = CacheVisitFactory()
        headers = get_headers_for_user(logged_in_user, User.Role.Default)
        response = self._send_put_request(client, cache_visit.id_, headers, _put_data)

        assert response.status_code == 403

    def test_put_other_users_cache_visit_by_admin(self, client, _put_data,
                                                  logged_in_user):
        cache_visit = CacheVisitFactory()
        headers = get_headers_for_user(logged_in_user, User.Role.Admin)
        response = self._send_put_request(client, cache_visit.id_, headers, _put_data)

        assert response.status_code == 200

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put(self, logged_in_user_role, client, _put_data_dict, logged_in_user):
        user, *_ = logged_in_user
        _put_data = json.dumps(_put_data_dict)
        cache_visit = CacheVisitFactory(user=user, rating=666)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(client, cache_visit.id_, headers, _put_data)

        assert response.status_code == 200
        for key, value in _put_data_dict.items():
            assert getattr(cache_visit, key) == value

    @pytest.mark.parametrize("attr_name", ("user", "cache"))
    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put_related_object_deleted(self, attr_name, logged_in_user_role, client,
                                        _put_data, logged_in_user):
        user, *_ = logged_in_user
        cache_visit = CacheVisitFactory(user=user)
        getattr(cache_visit, attr_name).deleted = True

        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(client, cache_visit.id_, headers, _put_data)

        assert response.status_code == 404


class TestCacheVisitDelete:

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_delete_cache_visit_not_found(self, logged_in_user_role, client,
                                          logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.delete("/api/cache_visits/2", headers=headers)

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_delete_cache_visit_deleted(self, logged_in_user_role, client,
                                        logged_in_user):
        cache_visit = CacheVisitFactory(deleted=True)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.get(f"/api/cache_visits/{cache_visit.id_}", headers=headers)

        assert response.status_code == 404

    def test_delete_unauthorized(self, client):
        cache_visit = CacheVisitFactory()

        response = client.delete(f"/api/cache_visits/{cache_visit.id_}")

        assert response.status_code == 401
        assert cache_visit.deleted is False

    def test_delete_other_users_visit(self, client, logged_in_user):
        cache_visit = CacheVisitFactory()
        headers = get_headers_for_user(logged_in_user, User.Role.Default)

        response = client.delete(f"/api/cache_visits/{cache_visit.id_}",
                                 headers=headers)

        assert response.status_code == 403
        assert cache_visit.deleted is False

    def test_delete_other_users_visit_by_admin(self, client, logged_in_user):
        cache_visit = CacheVisitFactory()
        headers = get_headers_for_user(logged_in_user, User.Role.Admin)

        response = client.delete(f"/api/cache_visits/{cache_visit.id_}",
                                 headers=headers)

        assert response.status_code == 200
        assert cache_visit.deleted is True

    def test_delete(self, client, logged_in_user):
        user, *_ = logged_in_user
        cache_visit = CacheVisitFactory(user=user)
        headers = get_headers_for_user(logged_in_user, User.Role.Default)

        response = client.delete(f"/api/cache_visits/{cache_visit.id_}",
                                 headers=headers)

        assert response.status_code == 200
        assert cache_visit.deleted is True
