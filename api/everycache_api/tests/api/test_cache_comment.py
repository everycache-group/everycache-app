import json

import pytest
from everycache_api.api.schemas.cache_comment import CacheCommentSchema
from everycache_api.models import CacheComment, User
from everycache_api.tests.factories.cache_comment_factory import \
    CacheCommentFactory
from everycache_api.tests.helpers import get_headers_for_user


class TestCacheCommentGet:

    def test_get_cache_comment_not_found(self, client):
        response = client.get("/api/cache_comments/2")

        assert response.status_code == 404

    def test_get_cache_comment_deleted(self, client):
        cache_comment = CacheCommentFactory(deleted=True)

        response = client.get(f"/api/cache_comments/{cache_comment.ext_id}")

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", (None, *list(User.Role)))
    def test_get(self, logged_in_user_role, client, logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        cache_comment = CacheCommentFactory()

        response = client.get(
            f"/api/cache_comments/{cache_comment.ext_id}", headers=headers)

        assert CacheComment.query.count() == 1
        db_comment = CacheComment.query.first()
        expected_data = json.loads(CacheCommentSchema().dumps(db_comment))

        assert response.status_code == 200
        assert response.json["cache_comment"] == expected_data

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_get_cache_deleted(self, logged_in_user_role, client,
                               logged_in_user):
        cache_comment = CacheCommentFactory()
        cache_comment.cache.deleted = True

        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.get(
            f"/api/cache_comments/{cache_comment.ext_id}", headers=headers)

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_get_author_deleted(self, logged_in_user_role, client,
                                logged_in_user):
        cache_comment = CacheCommentFactory()
        cache_comment.author.deleted = True

        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.get(
            f"/api/cache_comments/{cache_comment.ext_id}", headers=headers)

        assert response.status_code == 200
        assert "cache_comment" in response.json


class TestCacheCommentPut:

    @pytest.fixture()
    def _put_data_dict(self):
        return {
            "text": "lorem ipsum",
        }

    @pytest.fixture()
    def _put_data(self, _put_data_dict):
        return json.dumps(_put_data_dict)

    def _send_put_request(self, client, cache_comment_id, headers, put_data):
        return client.put(
            f"/api/cache_comments/{cache_comment_id}",
            content_type="application/json",
            headers=headers,
            data=put_data)

    def test_put_unauthorized(self, client, _put_data):
        cache_comment = CacheCommentFactory()

        response = self._send_put_request(client, cache_comment.ext_id, {}, _put_data)

        assert response.status_code == 401

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put_cache_comment_not_found(self, logged_in_user_role, client, _put_data,
                                         logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(client, 2, headers, _put_data)

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put_cache_comment_deleted(self, logged_in_user_role, client, _put_data,
                                       logged_in_user):
        cache_comment = CacheCommentFactory(deleted=True)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(
            client, cache_comment.ext_id, headers, _put_data)

        assert response.status_code == 404

    def test_put_other_users_cache_comment(self, client, _put_data, logged_in_user):
        cache_comment = CacheCommentFactory()
        headers = get_headers_for_user(logged_in_user, User.Role.Default)
        response = self._send_put_request(
            client, cache_comment.ext_id, headers, _put_data)

        assert response.status_code == 403

    def test_put_other_users_cache_comment_by_admin(self, client, _put_data,
                                                    logged_in_user):
        cache_comment = CacheCommentFactory()
        headers = get_headers_for_user(logged_in_user, User.Role.Admin)
        response = self._send_put_request(
            client, cache_comment.ext_id, headers, _put_data)

        assert response.status_code == 200

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put(self, logged_in_user_role, client, _put_data_dict, logged_in_user):
        user, *_ = logged_in_user
        _put_data = json.dumps(_put_data_dict)
        cache_comment = CacheCommentFactory(author=user)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(
            client, cache_comment.ext_id, headers, _put_data)

        assert response.status_code == 200
        for key, value in _put_data_dict.items():
            assert getattr(cache_comment, key) == value

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put_by_deleted_user(self, logged_in_user_role, client, _put_data_dict,
                                 logged_in_user):
        user, *_ = logged_in_user
        user.deleted = True

        _put_data = json.dumps(_put_data_dict)
        cache_comment = CacheCommentFactory(author=user)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(
            client, cache_comment.ext_id, headers, _put_data)

        assert response.status_code == 401
        for key, value in _put_data_dict.items():
            assert getattr(cache_comment, key) != value

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_put_cache_deleted(self, logged_in_user_role, client,
                               _put_data, logged_in_user):
        user, *_ = logged_in_user
        cache_comment = CacheCommentFactory(author=user)
        cache_comment.cache.deleted = True

        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = self._send_put_request(
            client, cache_comment.ext_id, headers, _put_data)

        assert response.status_code == 404


class TestCacheCommentDelete:

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_delete_cache_comment_not_found(self, logged_in_user_role, client,
                                            logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.delete("/api/cache_comments/2", headers=headers)

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_delete_cache_comment_deleted(self, logged_in_user_role, client,
                                          logged_in_user):
        cache_comment = CacheCommentFactory(deleted=True)
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.get(
            f"/api/cache_comments/{cache_comment.ext_id}", headers=headers)

        assert response.status_code == 404

    def test_delete_unauthorized(self, client):
        cache_comment = CacheCommentFactory()

        response = client.delete(f"/api/cache_comments/{cache_comment.ext_id}")

        assert response.status_code == 401
        assert cache_comment.deleted is False

    def test_delete_other_users_visit(self, client, logged_in_user):
        cache_comment = CacheCommentFactory()
        headers = get_headers_for_user(logged_in_user, User.Role.Default)

        response = client.delete(f"/api/cache_comments/{cache_comment.ext_id}",
                                 headers=headers)

        assert response.status_code == 403
        assert cache_comment.deleted is False

    def test_delete_other_users_visit_by_admin(self, client, logged_in_user):
        cache_comment = CacheCommentFactory()
        headers = get_headers_for_user(logged_in_user, User.Role.Admin)

        response = client.delete(f"/api/cache_comments/{cache_comment.ext_id}",
                                 headers=headers)

        assert response.status_code == 200
        assert cache_comment.deleted is True

    def test_delete(self, client, logged_in_user):
        user, *_ = logged_in_user
        cache_comment = CacheCommentFactory(author=user)
        headers = get_headers_for_user(logged_in_user, User.Role.Default)

        response = client.delete(f"/api/cache_comments/{cache_comment.ext_id}",
                                 headers=headers)

        assert response.status_code == 200
        assert cache_comment.deleted is True

    def test_delete_by_deleted_user(self, client, logged_in_user):
        user, *_ = logged_in_user
        user.deleted = True
        cache_comment = CacheCommentFactory(author=user)
        headers = get_headers_for_user(logged_in_user, User.Role.Default)

        response = client.delete(f"/api/cache_comments/{cache_comment.ext_id}",
                                 headers=headers)

        assert response.status_code == 401
        assert cache_comment.deleted is False
