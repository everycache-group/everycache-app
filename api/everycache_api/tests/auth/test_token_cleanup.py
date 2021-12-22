from everycache_api.models import Token
from everycache_api.auth.token_cleanup import cleanup_expired_tokens, add_token_cleanup_job
from everycache_api.tests.factories.token_factory import TokenFactory
from datetime import datetime, timedelta


def test_token_cleanup(app, mocker):
    mock = mocker.patch("everycache_api.auth.token_cleanup.apscheduler")
    mock.app = app
    token_1 = TokenFactory()
    TokenFactory(expires=datetime.utcnow() - timedelta(days=1))
    TokenFactory(expires=datetime.utcnow() - timedelta(seconds=50))
    jti = token_1.jti

    assert Token.query.count() > 1

    cleanup_expired_tokens()

    assert Token.query.count() == 1
    token = Token.query.first()
    assert token.jti == jti


def test_token_cleanup_none_found(app, mocker):
    mock = mocker.patch("everycache_api.auth.token_cleanup.apscheduler")
    mock.app = app
    cleanup_expired_tokens()


def test_add_job(mocker):
    mock = mocker.patch("everycache_api.auth.token_cleanup.apscheduler")

    add_token_cleanup_job()

    mock.add_job.assert_called_once()
