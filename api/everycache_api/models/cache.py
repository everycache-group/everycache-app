from datetime import datetime

from sqlalchemy.sql.expression import cast, func
from sqlalchemy.types import Float
from sqlalchemy_utils.aggregates import aggregated

from everycache_api.extensions import db

from .base import BaseMixin
from .cache_visit import CacheVisit


class Cache(BaseMixin, db.Model):
    __tablename__ = "caches"

    # own properties
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lon = db.Column(db.Numeric(scale=4, asdecimal=True), nullable=False)
    lat = db.Column(db.Numeric(scale=4, asdecimal=True), nullable=False)

    @aggregated("visits", db.Column(db.Float))
    def rating(self):
        return cast(func.sum(CacheVisit.rating), Float) / func.count(CacheVisit.id_)

    # foreign keys
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # relationships
    owner = db.relationship("User", uselist=False, back_populates="owned_caches")
    visits = db.relationship("CacheVisit", uselist=True, back_populates="cache")
    comments = db.relationship("CacheComment", uselist=True, back_populates="cache")
