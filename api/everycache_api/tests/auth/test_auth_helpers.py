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
from everycache_api.tests.factories.token_factory import TokenFactory
from everycache_api.tests.factories.user_factory import AdminFactory, UserFactory


TOKEN_TYPES = ("access", "refresh")


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
def test_save_encoded_token(token_type, mocker):
    user = UserFactory()
    decoded_token = {
        "jti": "test_jti",
        "exp": datetime.now().timestamp(),
        "type": token_type,
        "sub": user.ext_id
    }
    mocker.patch("everycache_api.auth.helpers.decode_token",
                 return_value=decoded_token)

    token = create_user_access_token(user)
    result = save_encoded_token(token)
    assert result

    assert Token.query.count() == 1
    token = Token.query.first()

    assert token.jti == decoded_token["jti"]
    assert token.token_type == decoded_token["type"]
    assert token.user_id == user.id_
    assert token.expires == datetime.fromtimestamp(decoded_token["exp"])
    assert token.revoked is False


@pytest.mark.parametrize("revoked", (True, False))
@pytest.mark.parametrize("token_type", TOKEN_TYPES)
def test_is_token_revoked(revoked, token_type):
    token = TokenFactory(revoked=revoked, token_type=token_type)
    sub = token.user.ext_id
    res = is_token_revoked({"jti": token.jti, "type": token_type, "sub": sub})
    assert res == revoked


def test_is_token_revoked_not_found():
    with pytest.raises(Exception):
        is_token_revoked({"jti": "t_jti", "type": "t_tt", "sub": "t_sub"})


@pytest.mark.parametrize("token_type", TOKEN_TYPES)
def test_revoke_token(token_type):
    token = TokenFactory(token_type=token_type)
    assert token.revoked is False

    revoke_token(
        {"jti": token.jti, "sub": token.user.ext_id, "type": token_type})

    assert token.revoked is True


def test_revoke_token_no_token():
    with pytest.raises(Exception):
        revoke_token({"jti": "jti", "sub": "ext_id", "type": "token_type"})


@pytest.mark.parametrize("token_type", TOKEN_TYPES)
def test_revoke_one_token(token_type):
    token_1 = TokenFactory(token_type=token_type)
    token_2 = TokenFactory(user=token_1.user, token_type=token_type)

    assert not token_1.revoked
    assert not token_2.revoked

    revoke_token(
        {"jti": token_2.jti, "sub": token_2.user.ext_id, "type": token_type})

    assert not token_1.revoked
    assert token_2.revoked


def test_revoke_all_user_tokens():
    user_1 = UserFactory()
    token_1 = TokenFactory(user=user_1)
    token_2 = TokenFactory(user=user_1)

    assert not any((token_1.revoked, token_2.revoked))

    revoke_all_user_tokens(user_1)

    assert all((token_1.revoked, token_2.revoked))


def test_revoke_all_user_tokens_other_users():
    user_1 = UserFactory()
    user_2 = UserFactory()
    token_1 = TokenFactory(user=user_1)
    token_2 = TokenFactory(user=user_1)
    token_3 = TokenFactory(user=user_2)

    assert not any((token_1.revoked, token_2.revoked, token_3.revoked))

    revoke_all_user_tokens(user_1)

    assert all((token_1.revoked, token_2.revoked))
    assert not token_3.revoked


def test_revoke_all_user_tokens_none_found():
    user_1 = UserFactory()
    assert revoke_all_user_tokens(user_1)
