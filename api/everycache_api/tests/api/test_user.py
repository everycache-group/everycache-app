import json

import pytest

from everycache_api.api.schemas.user import PublicUserSchema, UserSchema
from everycache_api.models import User
from everycache_api.tests.factories.user_factory import UserFactory


class TestGet:

    def test_get_public(self, client):
        user = UserFactory()
        response = client.get(f"/api/users/{user.username}")

        assert response.json == {"user": json.loads(PublicUserSchema().dumps(user))}
        assert response.status_code == 200

    def test_get_self(self, client, logged_in_user):
        user, access_token, _ = logged_in_user
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"/api/users/{user.username}",
                              content_type="application/json", headers=headers)

        assert response.json == {"user": json.loads(UserSchema().dumps(user))}
        assert response.status_code == 200

    def test_get_other_user(self, client, logged_in_user):
        user_1 = UserFactory()
        user_2, access_token, _ = logged_in_user
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"/api/users/{user_1.username}",
                              content_type="application/json", headers=headers)

        assert response.json == {"user": json.loads(PublicUserSchema().dumps(user_1))}
        assert response.status_code == 200

    def test_get_no_user(self, client):
        response = client.get("/api/users/username", content_type="application/json")

        assert response.status_code == 404

    def test_get_admin(self, client, logged_in_user):
        user, access_token, _ = logged_in_user
        user.role = User.Role.Admin
        user_2 = UserFactory()

        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"/api/users/{user_2.username}",
                              content_type="application/json", headers=headers)
        assert response.json == {"user": json.loads(UserSchema().dumps(user_2))}
        assert response.status_code == 200


class TestPut:

    def _get_user_edit_data(self, user):
        return json.dumps({
            "username": "changed_username",
            "email": user.email,
            "password": f"testpass{user.id_}"
        })

    def _validate_put_successful(self, response, user):
        assert response.status_code == 200
        assert response.json["user"]["username"] == "changed_username"
        assert user.username == "changed_username"

    def _send_put_request(self, client, user_to_be_changed, access_token):
        user = user_to_be_changed
        return client.put(
            f"/api/users/{user.username}",
            data=self._get_user_edit_data(user),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"})

    def test_put_self(self, client, logged_in_user):
        user, access_token, _ = logged_in_user

        response = self._send_put_request(client, user, access_token)
        self._validate_put_successful(response, user)

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

        response = self._send_put_request(client, user_2, access_token)
        self._validate_put_successful(response, user_2)

    def test_put_user_not_found(self, client, logged_in_user):
        user, access_token, _ = logged_in_user
        user.role = User.Role.Admin

        response = client.put(
            "/api/users/some_other_username",
            data=self._get_user_edit_data(user),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"})

        assert response.status_code == 404


class TestDelete:

    @pytest.fixture()
    def mocked_token_revoke(self, mocker):
        return mocker.patch("everycache_api.api.resources.user.revoke_all_user_tokens")

    def _validate_delete_successful(self, response, user, mocked_token_revoke):
        assert response.status_code == 200
        assert user.deleted is True
        mocked_token_revoke.assert_called_once()

    def _send_delete_request(self, client, user_to_be_deleted, access_token):
        return client.delete(
            f"/api/users/{user_to_be_deleted.username}",
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"})

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
        mocked_token_revoke.assert_not_called()

    def test_delete_other_user_by_admin(self, client, logged_in_user,
                                        mocked_token_revoke):
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
            "/api/users/some_username", content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"})

        assert response.status_code == 404
        mocked_token_revoke.assert_not_called()


class TestListGet:

    @pytest.mark.parametrize("is_user_logged_in", (False, True))
    def test_get_public_list(self, is_user_logged_in, client, logged_in_user):
        user, access_token, _ = logged_in_user
        for _ in range(5):
            UserFactory()

        headers = {}
        if is_user_logged_in:
            headers = {"Authorization": f"Bearer {access_token}"}

        response = client.get("/api/users", headers=headers)

        users = User.query.filter_by(verified=True)
        users_expected = json.loads(PublicUserSchema().dumps(users, many=True))
        assert response.json["results"] == users_expected
        assert response.json["results"] != []
        assert response.status_code == 200

    @pytest.mark.parametrize("is_user_logged_in", (False, True))
    def test_get_unverified_user_gets_hidden(self, is_user_logged_in, client,
                                             logged_in_user):
        user, access_token, _ = logged_in_user

        headers = {}
        if is_user_logged_in:
            headers = {"Authorization": f"Bearer {access_token}"}

        response = client.get("/api/users", headers=headers)
        assert response.json["results"] != []
        assert response.status_code == 200

        user.verified = False
        response = client.get("/api/users", headers=headers)
        assert response.json["results"] == []
        assert response.status_code == 200

    def test_get_admin_list(self, client, logged_in_user):
        user, access_token, _ = logged_in_user
        user.role = User.Role.Admin
        for _ in range(5):
            UserFactory()

        response = client.get(
            "/api/users", headers={"Authorization": f"Bearer {access_token}"})

        expected_users = json.loads(UserSchema().dumps(User.query.all(), many=True))

        assert response.json["results"] == expected_users
        assert response.status_code == 200

    def test_get_admin_sees_all(self, client, logged_in_user):
        user, access_token, _ = logged_in_user
        user.role = User.Role.Admin

        response = client.get(
            "/api/users", headers={"Authorization": f"Bearer {access_token}"})

        assert len(response.json["results"]) == 1
        assert response.status_code == 200

        UserFactory(verified=False)

        response = client.get(
            "/api/users", headers={"Authorization": f"Bearer {access_token}"})

        assert len(response.json["results"]) == 2
        assert response.status_code == 200


class TestListPost:

    @pytest.fixture()
    def user_to_create_data_dict(self):
        return {
            "username": "testowy",
            "password": "testpass",
            "email": "testowy@example.com",
            "role": "Default"}

    @pytest.fixture()
    def user_to_create_data(self, user_to_create_data_dict):
        return json.dumps(user_to_create_data_dict)

    def test_post(self, client, user_to_create_data):
        assert User.query.count() == 0

        response = client.post("/api/users", data=user_to_create_data,
                               content_type="application/json")

        assert response.status_code == 201
        assert "user created" in response.data.decode()
        user_query = User.query.filter_by(username="testowy")
        assert user_query.count() == 1
        user = user_query.first()

        assert user
        assert user.email == "testowy@example.com"
        assert user.role.name == "Default"

    def test_post_logged_in(self, client, user_to_create_data, logged_in_user):
        user, access_token, _ = logged_in_user

        response = client.post(
            "/api/users",
            data=user_to_create_data,
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"})

        assert response.status_code == 403
        assert "user already logged in" in response.data.decode()

    def test_post_logged_in_as_admin(self, client, user_to_create_data, logged_in_user):
        user, access_token, _ = logged_in_user
        user.role = User.Role.Admin

        response = client.post(
            "/api/users",
            data=user_to_create_data,
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"})

        assert response.status_code == 201
        assert "user created" in response.data.decode()

    @pytest.mark.parametrize("is_issued_by_admin", (True, False))
    @pytest.mark.parametrize("unique_field_name", ("username", "email"))
    def test_post_unique_value_taken(self, is_issued_by_admin, unique_field_name,
                                     client, user_to_create_data_dict, logged_in_user):
        user, access_token, _ = logged_in_user
        setattr(user, unique_field_name, user_to_create_data_dict[unique_field_name])
        user.role = User.Role.Admin

        assert User.query.count() == 1

        headers = {}
        if is_issued_by_admin:
            headers = {"Authorization": f"Bearer {access_token}"}

        response = client.post("/api/users", data=json.dumps(user_to_create_data_dict),
                               content_type="application/json", headers=headers)

        assert response.status_code == 400
        assert f"{unique_field_name} is already taken" in response.data.decode()
        assert User.query.count() == 1
