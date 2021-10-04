from datetime import datetime

import pytest

from everycache_api.auth.helpers import (
    add_token_to_database,
    create_jwt_payload,
    create_user_access_token,
    create_user_refresh_token,
    is_token_revoked,
    revoke_all_user_tokens,
    revoke_token,
)
from everycache_api.models import Token
from everycache_api.tests.factories.token_factory import TokenFactory
from everycache_api.tests.factories.user_factory import AdminFactory, UserFactory


@pytest.mark.parametrize("factory", (UserFactory, AdminFactory))
def test_create_jwt_payload(factory):
    user = factory()

    assert create_jwt_payload(user) == {"identity": user.id_, "additional_claims": {
        "role": user.role.value}}


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


def test_add_token_to_database(mocker):
    identity_claim = "id_claim"
    decoded_token = {
        "jti": "test_jti",
        "type": "test_token_type",
        identity_claim: 666,
        "exp": datetime.now().timestamp()
    }
    mocker.patch("everycache_api.auth.helpers.decode_token",
                 return_value=decoded_token)

    add_token_to_database(None, identity_claim)

    assert Token.query.count() == 1
    token = Token.query.first()

    assert token.jti == decoded_token["jti"]
    assert token.token_type == decoded_token["type"]
    assert token.user_id == decoded_token[identity_claim]
    assert token.expires == datetime.fromtimestamp(decoded_token["exp"])
    assert token.revoked is False


@pytest.mark.parametrize("revoked", (True, False))
def test_is_token_revoked(revoked):
    token = TokenFactory(revoked=revoked)
    assert is_token_revoked({"jti": token.jti}) == revoked


def test_revoke_token():
    token = TokenFactory()
    assert token.revoked is False

    revoke_token(token.jti, token.user_id)

    assert token.revoked is True


def test_revoke_token_no_token():
    with pytest.raises(Exception):
        revoke_token("test_jti", 666)


def test_revoke_one_token():
    token_1 = TokenFactory()
    token_2 = TokenFactory(user=token_1.user)

    assert not token_1.revoked
    assert not token_2.revoked

    revoke_token(token_2.jti, token_2.user.id_)

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
