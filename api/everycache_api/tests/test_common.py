import pytest
from marshmallow import ValidationError
from everycache_api.api.resources.user import UserListResource
from everycache_api.app import create_app


def test_create_app():
    assert create_app("everycache_api.tests.test_config")


@pytest.mark.parametrize("endpoint", ("/api/users", "/api/caches"))
def test_request_list_empty_database(client, endpoint):
    response = client.get(endpoint)
    assert response.json == {
        "total": 0,
        "pages": 0,
        "next": f"{endpoint}?page=1&per_page=50",
        "prev": f"{endpoint}?page=1&per_page=50",
        "results": [],
    }


def test_marshmallow_error(client, mocker):
    msg = "test_marshmallow_error"
    mocker.patch.object(
        UserListResource,
        "get",
        side_effect=ValidationError(message=msg),
    )

    response = client.get("/api/users")
    assert response.json == [msg]
    assert response.status_code == 400
