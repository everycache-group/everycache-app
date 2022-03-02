from everycache_api.app import create_app


def test_redis_client_init(mocker):
    mock = mocker.patch("everycache_api.app.redis_client")

    create_app(None)
    mock.init_app.assert_called_once()
