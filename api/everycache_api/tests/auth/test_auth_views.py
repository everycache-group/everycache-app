import json
import flask_jwt_extended
import pytest
import everycache_api
from everycache_api.tests.factories.user_factory import UserFactory
from everycache_api.models import Token


@pytest.fixture
def valid_login_data():
    user = UserFactory()

    login_data = {"email": user.email, "password": f"testpass{user.id_}"}
    return json.dumps(login_data)


@pytest.fixture
def valid_token_pair(valid_login_data, client):
    response = client.post("/auth/login", data=valid_login_data, content_type="application/json")
    return response.json["access_token"], response.json["refresh_token"]


def test_login(client, valid_login_data):
    count_before = Token.query.count()
    response = client.post("/auth/login", data=valid_login_data, content_type="application/json")

    assert "access_token" in response.json
    assert "refresh_token" in response.json
    assert Token.query.count() == count_before + 2


def test_login_not_json(client, valid_login_data):
    response = client.post("/auth/login", data=valid_login_data)

    assert "Missing JSON payload in request" in response.data.decode()


def test_login_wrong_email(client):
    login_data = {"email": "invalid_email", "password": "testpass"}
    response = client.post("/auth/login", data=json.dumps(login_data), content_type="application/json")

    assert "Incorrect email and password combination" in response.data.decode()


def test_login_wrong_password(client):
    user = UserFactory()

    login_data = {"email": user.email, "password": "testpass_invalid"}
    response = client.post("/auth/login", data=json.dumps(login_data), content_type="application/json")

    assert "Incorrect email and password combination" in response.data.decode()


@pytest.mark.parametrize("login_data", (
    {"email": ""},
    {"password": ""},
    {}
))
def test_login_missing_data(client, login_data):
    response = client.post("/auth/login", data=json.dumps(login_data), content_type="application/json")

    assert "Missing e-mail address or password" in response.data.decode()


def test_refresh(client, valid_token_pair):
    _, valid_refresh_token = valid_token_pair
    count_before = Token.query.count()
    headers = {f"Authorization": f"Bearer {valid_refresh_token}"}
    response = client.post("/auth/refresh", content_type="application/json", headers=headers)

    assert "access_token" in response.json
    assert Token.query.count() == count_before + 1


def test_refresh_user_not_found(client, valid_token_pair, mocker):
    _, valid_refresh_token = valid_token_pair

    mocker.patch.object(everycache_api.auth.views, "current_user", None)

    headers = {f"Authorization": f"Bearer {valid_refresh_token}"}
    response = client.post("/auth/refresh", content_type="application/json", headers=headers)

    assert response.json == {"msg": "User in refresh token does not exist"}


def test_revoke_access_token(client, valid_token_pair, mocker):
    access_token, _ = valid_token_pair

    headers = {f"Authorization": f"Bearer {access_token}"}
    mock = mocker.patch("everycache_api.auth.views.revoke_token")
    response = client.delete("/auth/revoke_access", content_type="application/json", headers=headers)
    assert response.json["message"] == "token revoked"
    mock.assert_called_once()


def test_revoke_refresh_token(client, valid_token_pair, mocker):
    _, refresh_token = valid_token_pair

    headers = {f"Authorization": f"Bearer {refresh_token}"}
    mock = mocker.patch("everycache_api.auth.views.revoke_token")
    response = client.delete("/auth/revoke_refresh", content_type="application/json", headers=headers)
    assert response.json["message"] == "token revoked"
    mock.assert_called_once()
