import json

import pytest

from everycache_api.api.schemas.cache import CachePublicSchema, CacheSchema
from everycache_api.api.schemas.cache_comment import CacheCommentSchema
from everycache_api.api.schemas.cache_visit import CacheVisitSchema
from everycache_api.extensions import db
from everycache_api.models import Cache, CacheComment, CacheVisit, User
from everycache_api.tests.factories.cache_comment_factory import CacheCommentFactory
from everycache_api.tests.factories.cache_factory import CacheFactory
from everycache_api.tests.factories.cache_visit_factory import CacheVisitFactory
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
        response = client.get(f"/api/caches/{cache.ext_id}", headers=headers)

        assert response.status_code == 404

    def test_get_cache_other_user_public(
        self, client
    ):
        cache = CacheFactory()

        response = client.get(f"/api/caches/{cache.ext_id}")

        cache = Cache.query.filter_by(id_=cache.id_).first()
        cache_deserialized = json.loads(CachePublicSchema().dumps(cache))
        assert response.status_code == 200
        assert response.json["cache"] == cache_deserialized

    def test_get_other_user_cache_by_admin(self, client, logged_in_user):
        cache = CacheFactory()
        headers = get_headers_for_user(logged_in_user, User.Role.Admin)

        response = client.get(f"/api/caches/{cache.ext_id}", headers=headers)

        assert response.status_code == 200
        cache = Cache.query.filter_by(id_=cache.id_).first()
        cache_deserialized = json.loads(CacheSchema().dumps(cache))

        assert response.json["cache"] == cache_deserialized

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_get_own_cache(self, logged_in_user_role, client, logged_in_user):
        user, *_ = logged_in_user
        cache = CacheFactory(owner=user)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.get(f"/api/caches/{cache.ext_id}", headers=headers)

        assert response.status_code == 200
        cache = Cache.query.filter_by(id_=cache.id_).first()
        cache_deserialized = json.loads(CacheSchema().dumps(cache))

        assert response.json["cache"] == cache_deserialized


class TestCachePut:
    @pytest.fixture()
    def _put_data_dict(self):
        return {"lon": 2.3, "lat": 4.3, "name": "new_cache_name"}

    @pytest.fixture()
    def _put_data(self, _put_data_dict):
        return json.dumps(_put_data_dict)

    def _send_put_request(self, client, put_data, headers, cache_id):
        return client.put(
            f"/api/caches/{cache_id}",
            headers=headers,
            content_type="application/json",
            data=put_data,
        )

    def test_put_unauthorized(self, client, _put_data):
        cache = CacheFactory()
        response = self._send_put_request(client, _put_data, {}, cache.ext_id)

        assert response.status_code == 401

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put_cache_not_found(
        self, logged_in_user_role, _put_data, client, logged_in_user
    ):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(client, _put_data, headers, 2)

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put_cache_deleted(
        self, logged_in_user_role, _put_data, client, logged_in_user
    ):
        user, *_ = logged_in_user
        cache = CacheFactory(deleted=True, owner=user)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(client, _put_data, headers, cache.ext_id)
        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put_own_cache(
        self, logged_in_user_role, _put_data_dict, client, logged_in_user
    ):
        user, *_ = logged_in_user
        cache = CacheFactory(owner=user)

        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(
            client, json.dumps(_put_data_dict), headers, cache.ext_id
        )

        assert response.status_code == 200
        for key, value in _put_data_dict.items():
            assert type(value)(getattr(cache, key)) == value

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put_own_cache_by_deleted_user(
        self, logged_in_user_role, _put_data_dict, client, logged_in_user
    ):
        user, *_ = logged_in_user
        user.deleted = True
        cache = CacheFactory(owner=user)

        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(
            client, json.dumps(_put_data_dict), headers, cache.ext_id
        )

        assert response.status_code == 401
        for key, value in _put_data_dict.items():
            assert type(value)(getattr(cache, key)) != value

    def test_put_other_users_cache(self, client, _put_data, logged_in_user):
        cache = CacheFactory()
        init_name = cache.name
        headers = get_headers_for_user(logged_in_user, User.Role.Default)
        response = self._send_put_request(client, _put_data, headers, cache.ext_id)

        assert response.status_code == 403
        assert cache.name == init_name

    def test_put_other_users_cache_by_admin(self, client, _put_data, logged_in_user):
        cache = CacheFactory()
        init_name = cache.name
        headers = get_headers_for_user(logged_in_user, User.Role.Admin)
        response = self._send_put_request(client, _put_data, headers, cache.ext_id)

        assert response.status_code == 200
        assert cache.name != init_name


class TestCacheDelete:
    def test_delete_unauthorized(self, client):
        cache = CacheFactory()
        response = client.delete(f"/api/caches/{cache.ext_id}")

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
        response = client.delete(f"/api/caches/{cache.ext_id}", headers=headers)
        assert response.status_code == 404

    def test_delete_other_users_cache(self, client, logged_in_user):
        cache = CacheFactory()
        headers = get_headers_for_user(logged_in_user, User.Role.Default)

        response = client.delete(f"/api/caches/{cache.ext_id}", headers=headers)

        assert response.status_code == 403
        assert cache.deleted is False
        db.session.refresh(cache)

    def test_delete_other_users_cache_by_admin(self, client, logged_in_user):
        cache = CacheFactory()
        headers = get_headers_for_user(logged_in_user, User.Role.Admin)

        response = client.delete(f"/api/caches/{cache.ext_id}", headers=headers)

        assert response.status_code == 200
        assert cache.deleted is True
        db.session.refresh(cache)

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_delete_own_cache(self, logged_in_user_role, client, logged_in_user):
        user, *_ = logged_in_user
        cache = CacheFactory(owner=user)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.delete(f"/api/caches/{cache.ext_id}", headers=headers)

        assert response.status_code == 200
        assert cache.deleted is True
        db.session.refresh(cache)

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_delete_own_cache_by_deleted_user(
        self, logged_in_user_role, client, logged_in_user
    ):
        user, *_ = logged_in_user
        user.deleted = True
        cache = CacheFactory(owner=user)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.delete(f"/api/caches/{cache.ext_id}", headers=headers)

        assert response.status_code == 401
        assert cache.deleted is False
        db.session.refresh(cache)


class TestCacheListGet:
    def test_get_public_list(self, client):
        cache = CacheFactory()
        for _ in range(5):
            CacheFactory()

        headers = {}
        response = client.get("/api/caches", headers=headers)

        caches = Cache.query.all()
        caches_expected = json.loads(CachePublicSchema().dumps(caches, many=True))
        assert cache in caches
        assert response.json["results"] == caches_expected
        assert response.status_code == 200

    def test_get_admin_list(self, client, logged_in_user):
        for _ in range(5):
            CacheFactory()

        headers = get_headers_for_user(logged_in_user, User.Role.Admin)
        response = client.get("/api/caches", headers=headers)

        expected_caches = json.loads(CacheSchema().dumps(Cache.query.all(), many=True))

        assert response.json["results"] == expected_caches
        assert response.status_code == 200

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_get_deleted_cache_hidden(
        self, logged_in_user_role, client, logged_in_user
    ):
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
            "name": "new_cache_name",
            "description": "new_cache_description",
        }

    @pytest.fixture()
    def _post_data(self, _post_data_dict):
        return json.dumps(_post_data_dict)

    def _send_post_request(self, client, post_data, headers):
        return client.post(
            "/api/caches",
            headers=headers,
            content_type="application/json",
            data=post_data,
        )

    def test_post_unauthorized(self, client, _post_data):
        assert Cache.query.count() == 0
        response = self._send_post_request(client, _post_data, {})

        assert response.status_code == 401
        assert Cache.query.count() == 0

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_post_cache_created(
        self, logged_in_user_role, client, _post_data_dict, logged_in_user
    ):
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


class TestCacheVisitListResourceGet:
    @pytest.mark.parametrize("logged_in_user_role", [None, *list(User.Role)])
    def test_get(self, logged_in_user_role, client, logged_in_user):
        cache = CacheFactory()
        cache_visit = CacheVisitFactory(cache=cache)
        CacheVisitFactory()
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.get(f"/api/caches/{cache.ext_id}/visits", headers=headers)

        db_visit = CacheVisit.query_ext_id(ext_id=cache_visit.ext_id).first()
        expected_visit = json.loads(CacheVisitSchema().dumps(db_visit))

        assert response.status_code == 200
        assert len(response.json["results"]) == 1
        assert response.json["results"] == [expected_visit]

    @pytest.mark.parametrize("logged_in_user_role", [None, *list(User.Role)])
    def test_get_cache_deleted(self, logged_in_user_role, client, logged_in_user):
        cache = CacheFactory()
        cache_visit = CacheVisitFactory(cache=cache)
        cache_visit.cache.deleted = True
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.get(f"/api/caches/{cache.ext_id}/visits", headers=headers)

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", [None, *list(User.Role)])
    def test_get_deleted(self, logged_in_user_role, client, logged_in_user):
        cache = CacheFactory()
        cache_visit = CacheVisitFactory(cache=cache)
        db.session.delete(cache_visit)
        CacheVisitFactory()
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.get(f"/api/caches/{cache.ext_id}/visits", headers=headers)

        assert response.status_code == 200
        assert len(response.json["results"]) == 0


class TestCacheVisitListResourcePost:
    def test_post_unauthorized(self, client):
        cache = CacheFactory()
        response = client.post(f"/api/caches/{cache.ext_id}/visits", headers={})
        assert response.status_code == 401
        assert CacheVisit.query.count() == 0

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_post_no_cache(self, logged_in_user_role, client, logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.post("/api/caches/cache_ext_id/visits", headers=headers)
        assert response.status_code == 404
        assert CacheVisit.query.count() == 0

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_post_cache_deleted(self, logged_in_user_role, client, logged_in_user):
        cache = CacheFactory(deleted=True)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.post(f"/api/caches/{cache.ext_id}/visits", headers=headers)
        assert response.status_code == 404
        assert CacheVisit.query.count() == 0

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_post(self, logged_in_user_role, client, logged_in_user):
        user, *_ = logged_in_user
        cache = CacheFactory()
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.post(
            f"/api/caches/{cache.ext_id}/visits",
            headers=headers,
            content_type="application/json",
            data=json.dumps({}),
        )

        assert response.status_code == 201
        assert CacheVisit.query.count() == 1
        visit = CacheVisit.query.first()
        assert visit.cache == cache
        assert visit.user == user


class TestCacheCommentListResourceGet:
    @pytest.mark.parametrize("logged_in_user_role", [None, *list(User.Role)])
    def test_get(self, logged_in_user_role, client, logged_in_user):
        cache_comment = CacheCommentFactory()
        CacheCommentFactory()
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.get(
            f"/api/caches/{cache_comment.cache.ext_id}/comments", headers=headers
        )

        db_comment = CacheComment.query_ext_id(ext_id=cache_comment.ext_id).first()
        expected_comment = json.loads(CacheCommentSchema().dumps(db_comment))

        assert response.status_code == 200
        assert len(response.json["results"]) == 1
        assert response.json["results"] == [expected_comment]

    @pytest.mark.parametrize("logged_in_user_role", [None, *list(User.Role)])
    def test_get_cache_deleted(self, logged_in_user_role, client, logged_in_user):
        cache = CacheFactory()
        cache_comment = CacheCommentFactory(cache=cache)
        cache_comment.cache.deleted = True
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.get(f"/api/caches/{cache.ext_id}/comments", headers=headers)

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", [None, *list(User.Role)])
    def test_get_deleted(self, logged_in_user_role, client, logged_in_user):
        cache = CacheFactory()
        cache_comment = CacheCommentFactory(cache=cache)
        cache_comment.deleted = True
        CacheCommentFactory()
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.get(f"/api/caches/{cache.ext_id}/comments", headers=headers)

        assert response.status_code == 200
        assert len(response.json["results"]) == 0


class TestCacheCommentListResourcePost:
    def test_post_unauthorized(self, client):
        cache = CacheFactory()
        response = client.post(f"/api/caches/{cache.ext_id}/comments", headers={})
        assert response.status_code == 401
        assert CacheComment.query.count() == 0

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_post_no_cache(self, logged_in_user_role, client, logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.post("/api/caches/cache_ext_id/comments", headers=headers)
        assert response.status_code == 404
        assert CacheComment.query.count() == 0

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_post_cache_deleted(self, logged_in_user_role, client, logged_in_user):
        cache = CacheFactory(deleted=True)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.post(f"/api/caches/{cache.ext_id}/comments", headers=headers)
        assert response.status_code == 404
        assert CacheComment.query.count() == 0

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_post(self, logged_in_user_role, client, logged_in_user):
        user, *_ = logged_in_user
        cache = CacheFactory()
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.post(
            f"/api/caches/{cache.ext_id}/comments",
            headers=headers,
            content_type="application/json",
            data=json.dumps({"text": "Example"}),
        )

        assert response.status_code == 201
        assert CacheComment.query.count() == 1
        comment = CacheComment.query.first()
        assert comment.cache == cache
        assert comment.author == user
