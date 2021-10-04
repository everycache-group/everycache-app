import json

import pytest

from everycache_api.api.schemas.user import PublicUserSchema, UserSchema
from everycache_api.models import User
from everycache_api.tests.factories.user_factory import UserFactory


def test_register(client):
    assert User.query.count() == 0

    user_data = {"username": "testowy", "password": "testpass",
                 "email": "testowy@example.com", "role": "Default"}

    response = client.post("/api/users", data=json.dumps(user_data),
                           content_type="application/json")
    assert "user created" in response.data.decode()

    user_query = User.query.filter_by(username="testowy")
    assert user_query.count() == 1
    user = user_query.first()
    assert user

    assert user.email == "testowy@example.com"
    assert user.role.name == "Default"
    assert response.status_code == 201


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
