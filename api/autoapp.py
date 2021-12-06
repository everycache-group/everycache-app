from flask_cors import CORS
from flask_migrate import upgrade

from everycache_api.app import create_app
from everycache_api.auth.storage_helper import load_tokens_from_database_to_storage
from everycache_api.auth.token_cleanup import add_token_cleanup_job
from everycache_api.config import FRONTEND_APP_URL
from everycache_api.extensions import apscheduler, redis_client

app = create_app()

with app.app_context():
    CORS(app, origin={FRONTEND_APP_URL})

    upgrade(directory="everycache_api/migrations/")

    add_token_cleanup_job()
    apscheduler.start()

    if redis_client:
        app.logger.info("Loading valid tokens from database to redis storage...")

        load_tokens_from_database_to_storage()

        app.logger.info("Done")
    else:
        app.logger.info("Running without redis, skipping loading tokens from database.")
