from flask_jwt_extended import JWTManager as BaseJWTManager
from sqlalchemy.exc import OperationalError


class JWTManager(BaseJWTManager):
    def init_app(self, app):
        init_res = super().init_app(app)
        with app.app_context():
            from everycache_api.auth.token_storage import load_tokens_from_db
            try:
                load_tokens_from_db(app)
            except OperationalError as e:
                app.logger.error(e)
        return init_res
