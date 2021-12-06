from flask_migrate import upgrade

from everycache_api.app import create_app, start_extensions

app = create_app()

with app.app_context():
    upgrade(directory="everycache_api/migrations/")

start_extensions(app)
