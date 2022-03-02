import json

import pytest

from everycache_api.api.schemas.cache import CachePublicSchema, CacheSchema
from everycache_api.api.schemas.cache_comment import CacheCommentSchema
from everycache_api.api.schemas.cache_visit import CacheVisitSchema
from everycache_api.api.schemas.user import UserPublicSchema, UserSchema
from everycache_api.extensions import db
from everycache_api.models import Cache, CacheComment, CacheVisit, User
from everycache_api.tests.factories.cache_comment_factory import CacheCommentFactory
from everycache_api.tests.factories.cache_factory import CacheFactory
from everycache_api.tests.factories.cache_visit_factory import CacheVisitFactory
from everycache_api.tests.factories.user_factory import UserFactory
from everycache_api.tests.helpers import get_auth_header, get_headers_for_user


class TestUserGet:
    def test_get_public(self, client):
        user = UserFactory()
        response = client.get(f"/api/users/{user.ext_id}")

        assert response.json == {"user": json.loads(UserPublicSchema().dumps(user))}
        assert response.status_code == 200

    def test_get_other_user(self, client, logged_in_user):
        user_1 = UserFactory()
        user_2, access_token, _ = logged_in_user
        headers = get_auth_header(access_token)
        response = client.get(
            f"/api/users/{user_1.ext_id}",
            content_type="application/json",
            headers=headers,
        )

        assert response.json == {"user": json.loads(UserPublicSchema().dumps(user_1))}
        assert response.status_code == 200

    def test_get_self(self, client, logged_in_user):
        user, access_token, _ = logged_in_user
        headers = get_auth_header(access_token)
        response = client.get(
            f"/api/users/{user.ext_id}",
            content_type="application/json",
            headers=headers,
        )

        assert response.json == {"user": json.loads(UserSchema().dumps(user))}
        assert response.status_code == 200

    def test_get_no_user(self, client):
        response = client.get("/api/users/username", content_type="application/json")

        assert response.status_code == 404

    def test_get_by_admin(self, client, logged_in_user):
        user, access_token, _ = logged_in_user
        user.role = User.Role.Admin
        user_2 = UserFactory()

        headers = get_auth_header(access_token)
        response = client.get(
            f"/api/users/{user_2.ext_id}",
            content_type="application/json",
            headers=headers,
        )
        assert response.json == {"user": json.loads(UserSchema().dumps(user_2))}
        assert response.status_code == 200

    @pytest.mark.parametrize("logged_in_user_role", (None, *list(User.Role)))
    def test_get_deleted_user(self, logged_in_user_role, client, logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        user = UserFactory()
        user.deleted = True

        response = client.get(
            f"/api/users/{user.ext_id}",
            content_type="application/json",
            headers=headers,
        )

        assert response.status_code == 404


class TestUserPut:
    current_password = None
    overwrite_current_password = False
    include_current_password = True

    @pytest.fixture(scope="class", autouse=True)
    def ensure_initial_settings(self):
        self.current_password = None
        self.overwrite_current_password = False
        self.include_current_password = True

    def _get_user_edit_data(self, user):
        data = {
                "username": "changed_username",
                "email": user.email,
                "password": f"testpass{user.id_}",
            }

        if self.overwrite_current_password:
            data["current_password"] = self.current_password
        elif self.include_current_password:
            data["current_password"] = f"testpass{user.id_}"

        return json.dumps(data)

    def _validate_put_successful(self, response, user):
        assert response.status_code == 200
        assert response.json["user"]["username"] == "changed_username"
        assert user.username == "changed_username"

    def _send_put_request(self, client, user_to_be_changed, access_token):
        user = user_to_be_changed
        return client.put(
            f"/api/users/{user.ext_id}",
            data=self._get_user_edit_data(user),
            content_type="application/json",
            headers=get_auth_header(access_token),
        )

    def test_put_self(self, client, logged_in_user):
        user, access_token, _ = logged_in_user

        response = self._send_put_request(client, user, access_token)
        self._validate_put_successful(response, user)

    def test_put_self_no_current_password(self, client, logged_in_user):
        user, access_token, _ = logged_in_user
        self.overwrite_current_password = True

        response = self._send_put_request(client, user, access_token)
        assert response.status_code == 400
        assert "Current password is required for updating user data." in response.json["errors"]["current_password"]

    def test_put_self_wrong_current_password(self, client, logged_in_user):
        user, access_token, _ = logged_in_user
        self.overwrite_current_password = True
        self.current_password = "nooo"

        response = self._send_put_request(client, user, access_token)
        assert response.status_code == 400
        assert "Current password is incorrect." in response.json["errors"]["current_password"]

    def test_put_other_user(self, client, logged_in_user):
        user, access_token, _ = logged_in_user
        user_2 = UserFactory()

        response = self._send_put_request(client, user_2, access_token)
        assert response.status_code == 403
        assert user.username != "changed_username"

    def test_put_other_user_by_admin(self, client, logged_in_user):
        user, access_token, _ = logged_in_user
        user.role = User.Role.Admin
        user_2 = UserFactory()
        self.include_current_password = False

        response = self._send_put_request(client, user_2, access_token)
        self._validate_put_successful(response, user_2)

    def test_put_user_not_found(self, client, logged_in_user):
        user, access_token, _ = logged_in_user
        user.role = User.Role.Admin

        response = client.put(
            "/api/users/some_other_username",
            data=self._get_user_edit_data(user),
            content_type="application/json",
            headers=get_auth_header(access_token),
        )

        assert response.status_code == 404


class TestUserDelete:
    @pytest.fixture()
    def mocked_token_revoke(self, mocker):
        return mocker.patch("everycache_api.api.resources.user.revoke_all_user_tokens")

    def _validate_delete_successful(self, response, user, mocked_token_revoke):
        assert response.status_code == 200
        assert user.deleted is True
        db.session.refresh(user)
        mocked_token_revoke.assert_called_once()

    def _send_delete_request(self, client, user_to_be_deleted, access_token):
        return client.delete(
            f"/api/users/{user_to_be_deleted.ext_id}",
            content_type="application/json",
            headers=get_auth_header(access_token),
        )

    def test_delete(self, client, logged_in_user, mocked_token_revoke):
        user, access_token, _ = logged_in_user

        assert user.deleted is False

        response = self._send_delete_request(client, user, access_token)

        self._validate_delete_successful(response, user, mocked_token_revoke)

    def test_delete_other_user(self, client, logged_in_user, mocked_token_revoke):
        user, access_token, _ = logged_in_user
        user_2 = UserFactory()

        assert user_2.deleted is False

        response = self._send_delete_request(client, user_2, access_token)

        assert response.status_code == 403
        assert user_2.deleted is False
        db.session.refresh(user)
        mocked_token_revoke.assert_not_called()

    def test_delete_other_user_by_admin(
        self, client, logged_in_user, mocked_token_revoke
    ):
        user, access_token, _ = logged_in_user
        user.role = User.Role.Admin
        user_2 = UserFactory()

        assert user_2.deleted is False

        response = self._send_delete_request(client, user_2, access_token)

        self._validate_delete_successful(response, user_2, mocked_token_revoke)

    def test_delete_user_not_found(self, client, logged_in_user, mocked_token_revoke):
        user, access_token, _ = logged_in_user
        user.role = User.Role.Admin

        response = client.delete(
            "/api/users/some_ext_id",
            content_type="application/json",
            headers=get_auth_header(access_token),
        )

        assert response.status_code == 404
        mocked_token_revoke.assert_not_called()


class TestUserListGet:
    @pytest.mark.parametrize("is_user_logged_in", (False, True))
    def test_get_public_list(self, is_user_logged_in, client, logged_in_user):
        user, access_token, _ = logged_in_user
        for _ in range(5):
            UserFactory()

        headers = {}
        if is_user_logged_in:
            headers = get_auth_header(access_token)

        response = client.get("/api/users", headers=headers)

        users = User.query.filter_by(verified=True)
        users_expected = json.loads(UserPublicSchema().dumps(users, many=True))
        assert user in users.all()
        assert response.json["results"] == users_expected
        assert response.status_code == 200

    @pytest.mark.parametrize("is_user_logged_in", (False, True))
    def test_get_unverified_user_gets_hidden(
        self, is_user_logged_in, client, logged_in_user
    ):
        user, access_token, _ = logged_in_user

        headers = {}
        if is_user_logged_in:
            headers = get_auth_header(access_token)

        response = client.get("/api/users", headers=headers)
        assert response.json["results"] != []
        assert response.status_code == 200

        user.verified = False
        response = client.get("/api/users", headers=headers)
        assert response.json["results"] == []
        assert response.status_code == 200

    @pytest.mark.parametrize("is_user_logged_in", (False, True))
    def test_get_deleted_user_gets_hidden(
        self, is_user_logged_in, client, logged_in_user
    ):
        _, access_token, _ = logged_in_user
        user = UserFactory()

        headers = {}
        if is_user_logged_in:
            headers = get_auth_header(access_token)

        response = client.get("/api/users", headers=headers)
        assert len(response.json["results"]) == 2
        assert response.status_code == 200

        user.deleted = True
        response = client.get("/api/users", headers=headers)
        assert len(response.json["results"]) == 1
        assert response.status_code == 200

    def test_get_admin_list(self, client, logged_in_user):
        user, access_token, _ = logged_in_user
        user.role = User.Role.Admin
        for _ in range(5):
            UserFactory()

        response = client.get("/api/users", headers=get_auth_header(access_token))

        expected_users = json.loads(UserSchema().dumps(User.query.all(), many=True))

        assert response.json["results"] == expected_users
        assert response.status_code == 200

    def test_get_admin_sees_all(self, client, logged_in_user):
        user, access_token, _ = logged_in_user
        user.role = User.Role.Admin

        response = client.get("/api/users", headers=get_auth_header(access_token))

        assert len(response.json["results"]) == 1
        assert response.status_code == 200

        UserFactory(verified=False)

        response = client.get("/api/users", headers=get_auth_header(access_token))

        assert len(response.json["results"]) == 2
        assert response.status_code == 200


class TestUserListPost:
    @pytest.fixture()
    def user_to_create_data_dict(self):
        return {
            "username": "testowy",
            "password": "testpass",
            "email": "testowy@example.com",
        }

    @pytest.fixture
    def mail_mock(self, mocker):
        return mocker.patch("everycache_api.api.resources.user.mail")

    @pytest.fixture()
    def user_to_create_data(self, user_to_create_data_dict):
        return json.dumps(user_to_create_data_dict)

    def test_post(self, client, user_to_create_data, mail_mock):
        assert User.query.count() == 0

        response = client.post(
            "/api/users", data=user_to_create_data, content_type="application/json"
        )

        assert response.status_code == 201
        assert "User created." in response.data.decode()
        user_query = User.query.filter_by(username="testowy")
        assert user_query.count() == 1
        user = user_query.first()

        assert user
        assert user.email == "testowy@example.com"
        assert user.role.name == "Default"
        mail_mock.send.assert_called_once()

    def test_post_logged_in(self, client, user_to_create_data, logged_in_user):
        user, access_token, _ = logged_in_user

        response = client.post(
            "/api/users",
            data=user_to_create_data,
            content_type="application/json",
            headers=get_auth_header(access_token),
        )

        assert response.status_code == 403
        assert "User already logged in." in response.data.decode()

    def test_post_logged_in_as_admin(self, client, user_to_create_data, logged_in_user, mail_mock):
        user, access_token, _ = logged_in_user
        user.role = User.Role.Admin

        response = client.post(
            "/api/users",
            data=user_to_create_data,
            content_type="application/json",
            headers=get_auth_header(access_token),
        )

        assert response.status_code == 201
        assert "User created." in response.data.decode()
        assert User.query.count() == 2
        mail_mock.send.assert_called_once()

    @pytest.mark.parametrize("is_issued_by_admin", (True, False))
    @pytest.mark.parametrize("unique_field_name", ("username", "email"))
    def test_post_unique_value_taken(
        self,
        is_issued_by_admin,
        unique_field_name,
        client,
        user_to_create_data_dict,
        logged_in_user,
    ):
        user, access_token, _ = logged_in_user
        setattr(user, unique_field_name, user_to_create_data_dict[unique_field_name])
        user.role = User.Role.Admin

        assert User.query.count() == 1

        headers = {}
        if is_issued_by_admin:
            headers = get_auth_header(access_token)

        response = client.post(
            "/api/users",
            data=json.dumps(user_to_create_data_dict),
            content_type="application/json",
            headers=headers,
        )

        assert response.status_code == 400
        assert f"{unique_field_name[0].upper()}{unique_field_name[1:]} is already taken." in response.data.decode()
        assert User.query.count() == 1


class TestUserCacheListGet:
    def test_get_public_list(self, client):
        cache = CacheFactory()
        CacheFactory()
        owner = cache.owner

        response = client.get(f"/api/users/{owner.ext_id}/caches")

        caches = Cache.query.filter_by(owner_id=owner.id_)
        expected_caches = json.loads(CachePublicSchema().dumps(caches, many=True))

        assert response.status_code == 200
        assert cache in caches.all()
        assert response.json["results"] == expected_caches

    @pytest.mark.parametrize("logged_in_user_role", (None, *list(User.Role)))
    def test_get_owner_not_found(self, logged_in_user_role, client, logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.get("/api/users/bogus_ext_id/caches", headers=headers)

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", (None, *list(User.Role)))
    def test_get_owner_deleted(self, logged_in_user_role, client, logged_in_user):
        cache = CacheFactory()
        cache.owner.deleted = True
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.get(
            f"/api/users/{cache.owner.ext_id}/caches", headers=headers
        )

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", (None, *list(User.Role)))
    def test_get_deleted_cache(self, logged_in_user_role, client, logged_in_user):
        cache = CacheFactory()

        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        response = client.get(
            f"/api/users/{cache.owner.ext_id}/caches", headers=headers
        )

        assert len(response.json["results"]) == 1

        cache.deleted = True

        response = client.get(
            f"/api/users/{cache.owner.ext_id}/caches", headers=headers
        )

        assert len(response.json["results"]) == 0

    def test_get_as_admin(self, client, logged_in_user):
        headers = get_headers_for_user(logged_in_user, User.Role.Admin)
        cache = CacheFactory()
        owner = cache.owner
        CacheFactory(owner=owner)
        CacheFactory()

        response = client.get(f"/api/users/{owner.ext_id}/caches", headers=headers)

        caches = Cache.query.filter_by(owner_id=owner.id_)
        expected_caches = json.loads(CacheSchema().dumps(caches, many=True))
        assert response.status_code == 200
        assert cache in caches.all()
        assert response.json["results"] == expected_caches

    def test_get_as_owner(self, client, logged_in_user):
        user, *_ = logged_in_user
        headers = get_headers_for_user(logged_in_user, User.Role.Default)
        cache = CacheFactory(owner=user)
        CacheFactory(owner=user)
        CacheFactory()

        response = client.get(f"/api/users/{user.ext_id}/caches", headers=headers)

        caches = Cache.query.filter_by(owner_id=user.id_)
        expected_caches = json.loads(CacheSchema(exclude=["visited"]).dumps(caches, many=True))
        assert response.status_code == 200
        assert cache in caches.all()
        assert response.json["results"] == expected_caches


class TestUserCacheVisitListGet:
    def _validate_success_for_user(self, client, user, access_token, cache_visit):
        response = client.get(
            f"/api/users/{user.ext_id}/visits", headers=get_auth_header(access_token)
        )

        cache_visits_for_user = CacheVisit.query.filter_by(user=user)
        expected_cache_visits = json.loads(
            CacheVisitSchema().dumps(cache_visits_for_user, many=True)
        )
        assert cache_visit in cache_visits_for_user.all()
        assert response.json["results"] == expected_cache_visits
        assert response.status_code == 200

    def test_get_unauthorized(self, client):
        response = client.get("/api/users/username/visits")
        assert response.status_code == 401

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_get_own_visits(self, logged_in_user_role, client, logged_in_user):
        user, access_token, _ = logged_in_user
        user.role = logged_in_user_role
        cache_visit = CacheVisitFactory(user=user)
        CacheVisitFactory()

        self._validate_success_for_user(client, user, access_token, cache_visit)

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_get_other_user_visits(self, logged_in_user_role, client, logged_in_user):
        logged_user, access_token, _ = logged_in_user
        logged_user.role = logged_in_user_role
        cache_visit = CacheVisitFactory()
        user = cache_visit.user
        cache_visit = CacheVisitFactory(user=user)
        CacheVisitFactory()

        self._validate_success_for_user(client, user, access_token, cache_visit)

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_get_no_user_found(self, logged_in_user_role, client, logged_in_user):
        logged_user, access_token, _ = logged_in_user
        logged_user.role = logged_in_user_role
        CacheVisitFactory()

        response = client.get(
            "/api/users/ext_id/visits", headers=get_auth_header(access_token)
        )

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_get_no_user_deleted(self, logged_in_user_role, client, logged_in_user):
        logged_user, access_token, _ = logged_in_user
        logged_user.role = logged_in_user_role
        cache_visit = CacheVisitFactory()
        user = cache_visit.user
        user.deleted = True

        response = client.get(
            f"/api/users/{user.ext_id}/visits", headers=get_auth_header(access_token)
        )

        assert response.status_code == 404

    @pytest.mark.parametrize("deleted_name", ("cache_visit", "cache"))
    @pytest.mark.parametrize("logged_in_user_role", list(User.Role))
    def test_get_deleted(
        self, deleted_name, logged_in_user_role, client, logged_in_user
    ):
        logged_user, access_token, _ = logged_in_user
        logged_user.role = logged_in_user_role
        cache_visit = CacheVisitFactory()
        if deleted_name == "cache_visit":
            cache_visit.deleted = True
        else:
            getattr(cache_visit, deleted_name).deleted = True

        response = client.get(
            f"/api/users/{cache_visit.user.ext_id}/visits",
            headers=get_auth_header(access_token),
        )

        assert response.status_code == 200
        assert response.json["results"] == []


class TestUserCacheCommentListGet:
    @pytest.mark.parametrize("logged_in_user_role", (None, *list(User.Role)))
    def test_get(self, logged_in_user_role, client, logged_in_user):
        cache_comment = CacheCommentFactory()
        CacheCommentFactory(author=cache_comment.author)
        CacheCommentFactory()

        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.get(
            f"/api/users/{cache_comment.author.ext_id}/comments", headers=headers
        )

        cache_comments_for_user = CacheComment.query.filter_by(
            author=cache_comment.author
        )
        expected_cache_comments = json.loads(
            CacheCommentSchema().dumps(cache_comments_for_user, many=True)
        )

        assert cache_comment in cache_comments_for_user.all()
        assert response.json["results"] == expected_cache_comments
        assert response.status_code == 200

    @pytest.mark.parametrize("logged_in_user_role", (None, *list(User.Role)))
    def test_get_user_not_found(self, logged_in_user_role, client, logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)

        response = client.get("/api/users/ext_id/comments", headers=headers)

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", (None, *list(User.Role)))
    def test_get_user_deleted(self, logged_in_user_role, client, logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        cache_comment = CacheCommentFactory()
        cache_comment.author.deleted = True

        response = client.get(
            f"/api/users/{cache_comment.author.ext_id}/comments", headers=headers
        )

        assert response.status_code == 404

    @pytest.mark.parametrize("logged_in_user_role", (None, *list(User.Role)))
    def test_get_cache_deleted(self, logged_in_user_role, client, logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        cache_comment = CacheCommentFactory()

        response = client.get(
            f"/api/users/{cache_comment.author.ext_id}/comments", headers=headers
        )

        assert len(response.json["results"]) == 1

        cache_comment.cache.deleted = True

        response = client.get(
            f"/api/users/{cache_comment.author.ext_id}/comments", headers=headers
        )

        assert len(response.json["results"]) == 0

    @pytest.mark.parametrize("logged_in_user_role", (None, *list(User.Role)))
    def test_get_comment_deleted(self, logged_in_user_role, client, logged_in_user):
        headers = get_headers_for_user(logged_in_user, logged_in_user_role)
        cache_comment = CacheCommentFactory()

        response = client.get(
            f"/api/users/{cache_comment.author.ext_id}/comments", headers=headers
        )

        assert len(response.json["results"]) == 1

        cache_comment.deleted = True
        response = client.get(
            f"/api/users/{cache_comment.author.ext_id}/comments", headers=headers
        )

        assert len(response.json["results"]) == 0
