import json
import os
import tempfile

import pytest
from flask import Flask
from flask_migrate import upgrade

from everycache_api.app import (
    configure_apispec,
    configure_extensions,
    register_blueprints,
)
from everycache_api.extensions import db
from everycache_api.tests.factories.user_factory import UserFactory


@pytest.fixture(scope="session")
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = Flask(__name__)
    app.config.from_object("everycache_api.tests.test_config")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    configure_extensions(app)
    configure_apispec(app)
    register_blueprints(app)

    with app.app_context():
        upgrade("everycache_api/migrations")
        yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="function", autouse=True)
def _db(app):
    db.create_all()
    yield db
    db.session.rollback()
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture()
def logged_in_user(client):
    user = UserFactory()
    login_data = json.dumps({"email": user.email, "password": f"testpass{user.id_}"})
    response = client.post("/auth/login", data=login_data,
                           content_type="application/json")
    return user, response.json["access_token"], response.json["refresh_token"]
