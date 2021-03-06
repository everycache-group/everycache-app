import json

import pytest

import everycache_api
from everycache_api.models import Token
from everycache_api.tests.factories.user_factory import UserFactory
from everycache_api.tests.helpers import get_auth_header


@pytest.fixture
def valid_login_data():
    user = UserFactory()

    login_data = {"email": user.email, "password": f"testpass{user.id_}"}
    return json.dumps(login_data)


@pytest.fixture
def valid_token_pair(valid_login_data, client):
    response = client.post("/auth/login", data=valid_login_data,
                           content_type="application/json")
    return response.json["access_token"], response.json["refresh_token"]


def test_login(client, valid_login_data):
    count_before = Token.query.count()
    response = client.post("/auth/login", data=valid_login_data,
                           content_type="application/json")

    assert "access_token" in response.json
    assert "refresh_token" in response.json
    assert response.status_code == 200
    assert Token.query.count() == count_before + 2


def test_login_not_json(client, valid_login_data):
    response = client.post("/auth/login", data=valid_login_data)

    assert "Missing JSON payload in request" in response.data.decode()
    assert response.status_code == 400


def test_login_wrong_email(client):
    login_data = {"email": "invalid_email", "password": "testpass"}
    response = client.post("/auth/login", data=json.dumps(login_data),
                           content_type="application/json")

    assert "Incorrect email and password combination" in response.data.decode()
    assert response.status_code == 401


def test_login_wrong_password(client):
    user = UserFactory()

    login_data = {"email": user.email, "password": "testpass_invalid"}
    response = client.post("/auth/login", data=json.dumps(login_data),
                           content_type="application/json")

    assert "Incorrect email and password combination" in response.data.decode()
    assert response.status_code == 401


@pytest.mark.parametrize("login_data", (
    {"email": ""},
    {"password": ""},
    {}
))
def test_login_missing_data(client, login_data):
    response = client.post("/auth/login", data=json.dumps(login_data),
                           content_type="application/json")

    if "email" not in login_data:
        assert "Missing data for required field." in response.json["errors"]["email"]
    if "password" not in login_data:
        assert "Missing data for required field." in response.json["errors"]["password"]
    assert response.status_code == 400


def test_refresh(client, valid_token_pair):
    _, valid_refresh_token = valid_token_pair
    count_before = Token.query.count()
    headers = get_auth_header(valid_refresh_token)
    response = client.post(
        "/auth/refresh", content_type="application/json", headers=headers)

    assert "access_token" in response.json
    assert Token.query.count() == count_before + 1
    assert response.status_code == 200


def test_refresh_user_not_found(client, valid_token_pair, mocker):
    _, valid_refresh_token = valid_token_pair

    mocker.patch.object(everycache_api.auth.views, "current_user", None)

    headers = get_auth_header(valid_refresh_token)
    response = client.post(
        "/auth/refresh", content_type="application/json", headers=headers)

    assert response.json == {"message": "Invalid or expired token."}
    assert response.status_code == 401


def test_revoke_access_token(client, valid_token_pair, mocker):
    access_token, _ = valid_token_pair

    headers = get_auth_header(access_token)
    mock = mocker.patch("everycache_api.auth.views.revoke_token")
    response = client.delete("/auth/revoke_access",
                             content_type="application/json", headers=headers)
    assert response.json["message"] == "Access token revoked."
    mock.assert_called_once()
    assert response.status_code == 200


def test_revoke_refresh_token(client, valid_token_pair, mocker):
    _, refresh_token = valid_token_pair

    headers = get_auth_header(refresh_token)
    mock = mocker.patch("everycache_api.auth.views.revoke_token")
    response = client.delete("/auth/revoke_refresh",
                             content_type="application/json", headers=headers)
    assert response.json["message"] == "Refresh token revoked."
    mock.assert_called_once()
    assert response.status_code == 200


def test_revoke_all(client, valid_token_pair, mocker):
    access_token, refresh_token = valid_token_pair

    headers = get_auth_header(access_token)
    mock = mocker.patch("everycache_api.auth.views.revoke_all_user_tokens")
    response = client.delete("/auth/revoke_all",
                             content_type="application/json", headers=headers)

    assert response.json["message"] == "All user tokens revoked."
    mock.assert_called_once()
    assert response.status_code == 200
