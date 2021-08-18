from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from everycache_api.app import create_app
from everycache_api.extensions import db

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_commmand("db", MigrateCommand)


if __name__ == "__main__":
    manager.run()
