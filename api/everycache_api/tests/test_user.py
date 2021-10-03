import json
from everycache_api.models import User


def test_register(client):
    assert User.query.count() == 0

    user_data = {"username": "testowy", "password": "testpass", "email": "testowy@example.com", "role": "Default"}

    response = client.post("/api/users", data=json.dumps(user_data), content_type="application/json")
    assert "user created" in response.data.decode()

    user_query = User.query.filter_by(username="testowy")
    assert user_query.count() == 1
    user = user_query.first()
    assert user

    assert user.email == "testowy@example.com"
    assert user.role.name == "Default"
