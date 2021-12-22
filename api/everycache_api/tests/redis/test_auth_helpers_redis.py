from datetime import datetime

import pytest

from everycache_api.auth.helpers import (
    create_jwt_payload,
    create_user_access_token,
    create_user_refresh_token,
    is_token_revoked,
    revoke_all_user_tokens,
    revoke_token,
    save_encoded_token,
)
from everycache_api.models import Token
from everycache_api.tests.factories.user_factory import AdminFactory, UserFactory
from everycache_api.auth.storage_helper import _format_token_key


TOKEN_TYPES = ("access", "refresh")


def push_one_token(redis_client, user, jti, token_type, expires=100):
    redis_key = _format_token_key(user.ext_id, token_type, jti)
    redis_client.set(redis_key, "noop".encode())
    redis_client.expire(redis_key, expires)

    return {"jti": jti, "type": token_type, "sub": user.ext_id}


@pytest.mark.parametrize("factory", (UserFactory, AdminFactory))
def test_create_jwt_payload(factory):
    user = factory()

    assert create_jwt_payload(user) == {"identity": user.ext_id, "additional_claims": {
        "role": user.role.name}}


def test_create_user_access_token(mocker):
    user = UserFactory()

    mock = mocker.patch("everycache_api.auth.helpers.create_access_token")
    create_user_access_token(user)

    mock.assert_called_once()


def test_create_user_refresh_token(mocker):
    user = UserFactory()

    mock = mocker.patch("everycache_api.auth.helpers.create_refresh_token")
    create_user_refresh_token(user)

    mock.assert_called_once()


@pytest.mark.parametrize("token_type", TOKEN_TYPES)
@pytest.mark.freeze_time
def test_save_encoded_token(token_type, mocker, redis_client):
    user = UserFactory()
    test_jti = "test_jti"
    expires = 50
    decoded_token = {
        "jti": test_jti,
        "exp": datetime.now().timestamp() + expires,
        "type": token_type,
        "sub": user.ext_id
    }
    mocker.patch("everycache_api.auth.helpers.decode_token",
                 return_value=decoded_token)

    token = create_user_access_token(user)
    result = save_encoded_token(token)
    assert result

    if token_type == "refresh":
        assert Token.query.count() == 1
        token = Token.query.first()

        assert token.jti == decoded_token["jti"]
        assert token.token_type == decoded_token["type"]
        assert token.user_id == user.id_
        assert token.expires == datetime.fromtimestamp(decoded_token["exp"])
        assert token.revoked is False
    else:
        assert Token.query.count() == 0

    redis_key = _format_token_key(user.ext_id, token_type, test_jti)
    result = redis_client.get(redis_key)

    assert result.decode() == "noop"
    assert redis_client.ttl(redis_key) == expires


@pytest.mark.parametrize("revoked", (True, False))
@pytest.mark.parametrize("token_type", TOKEN_TYPES)
def test_is_token_revoked(revoked, token_type, redis_client):
    test_jti = "test_jti"
    user = UserFactory()
    jwt_payload = push_one_token(
        redis_client, user, test_jti, token_type, int(not revoked))

    res = is_token_revoked(jwt_payload)
    assert res == revoked


def test_is_token_revoked_not_found():
    res = is_token_revoked({"jti": "t_jti", "type": "t_tt", "sub": "t_sub"})
    assert res is True


@pytest.mark.parametrize("token_type", TOKEN_TYPES)
def test_revoke_token(token_type, redis_client):
    user = UserFactory()
    test_jti = "test_jti"
    jwt_payload = push_one_token(redis_client, user, test_jti, token_type)

    assert is_token_revoked(jwt_payload) is False

    revoke_token(jwt_payload)

    assert is_token_revoked(jwt_payload) is True


def test_revoke_token_no_token():
    with pytest.raises(Exception):
        revoke_token({"jti": "jti", "sub": "ext_id", "type": "token_type"})


@pytest.mark.parametrize("token_type", TOKEN_TYPES)
def test_revoke_one_token(token_type, redis_client):
    user = UserFactory()
    test_jti_1 = "test_jti_1"
    test_jti_2 = "test_jti_2"
    jwt_payload_1 = push_one_token(redis_client, user, test_jti_1, token_type)
    jwt_payload_2 = push_one_token(redis_client, user, test_jti_2, token_type)

    assert not is_token_revoked(jwt_payload_1)
    assert not is_token_revoked(jwt_payload_2)

    revoke_token(jwt_payload_2)

    assert not is_token_revoked(jwt_payload_1)
    assert is_token_revoked(jwt_payload_2)


@pytest.mark.parametrize("token_type", TOKEN_TYPES)
def test_revoke_all_user_tokens(redis_client, token_type):
    user = UserFactory()
    test_jti_1 = "test_jti_1"
    test_jti_2 = "test_jti_2"
    jwt_payload_1 = push_one_token(redis_client, user, test_jti_1, token_type)
    jwt_payload_2 = push_one_token(redis_client, user, test_jti_2, token_type)

    assert not any((is_token_revoked(jwt_payload_1),
                    is_token_revoked(jwt_payload_2)))

    revoke_all_user_tokens(user)

    assert all((is_token_revoked(jwt_payload_1),
                is_token_revoked(jwt_payload_2)))


@pytest.mark.parametrize("token_type", TOKEN_TYPES)
def test_revoke_all_user_tokens_other_users(redis_client, token_type):
    user_1 = UserFactory()
    user_2 = UserFactory()
    test_jti_1 = "test_jti_1"
    test_jti_2 = "test_jti_2"
    test_jti_3 = "test_jti_2"
    jwt_payload_1 = push_one_token(
        redis_client, user_1, test_jti_1, token_type)
    jwt_payload_2 = push_one_token(
        redis_client, user_1, test_jti_2, token_type)
    jwt_payload_3 = push_one_token(
        redis_client, user_2, test_jti_3, token_type)

    payloads = (jwt_payload_1, jwt_payload_2, jwt_payload_3)
    assert not any(map(lambda x: is_token_revoked(x), payloads))

    revoke_all_user_tokens(user_1)

    assert all(map(lambda x: is_token_revoked(x), (jwt_payload_1,
                                                   jwt_payload_2)))
    assert not is_token_revoked(jwt_payload_3)


def test_revoke_all_user_tokens_none_found():
    user_1 = UserFactory()
    assert revoke_all_user_tokens(user_1)
