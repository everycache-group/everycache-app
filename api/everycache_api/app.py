import logging
from sys import stdout

from flask import Flask

from everycache_api import api, auth
from everycache_api.extensions import apispec, db, jwt, migrate, redis_client

from everycache_api.config import FRONTEND_APP_URL
from flask_cors import CORS

def create_app(config_object="everycache_api.config"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    CORS(app, origin={FRONTEND_APP_URL})
    app.config.from_object(config_object)

    configure_extensions(app)
    configure_apispec(app)
    register_blueprints(app)

    return app


def configure_extensions(app):
    """Configure flask extensions"""
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    if redis_client:
        redis_client.init_app(app)

    return True


def configure_apispec(app):
    """Configure APISpec for Swagger support"""
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )
    return True


def register_blueprints(app):
    """Configure all blueprints for app"""
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(auth.views.blueprint)
    return True


def configure_logger(app):
    """Configure logger"""
    if not app.logger.handlers:
        handler = logging.StreamHandler(stdout)
        app.logger.addHandler(handler)
