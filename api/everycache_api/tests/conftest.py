import os
import tempfile

import pytest
from flask_migrate import upgrade

from everycache_api.app import create_app


@pytest.fixture()
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app("everycache_api.tests.test_config")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    with app.test_client() as client:
        with app.app_context():
            upgrade("everycache_api/migrations")
        yield client

    os.close(db_fd)
    os.unlink(db_path)
