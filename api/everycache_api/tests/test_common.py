import pytest


@pytest.mark.parametrize("endpoint", ("/api/users", "/api/caches"))
def test_request_list_empty_database(client, endpoint):
    response = client.get(endpoint)
    assert response.json == {
        "total": 0,
        "pages": 0,
        "next": f"{endpoint}?page=1&per_page=50",
        "prev": f"{endpoint}?page=1&per_page=50",
        "results": []
    }
