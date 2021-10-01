from everycache_api.extensions import db


class BaseMixin(object):
    id_ = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    deleted = db.Column(db.Boolean, nullable=False, default=False)
