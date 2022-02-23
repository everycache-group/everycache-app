from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from everycache_api.extensions import db

from .base import BaseMixin


class Cache(BaseMixin, db.Model):
    __tablename__ = "caches"

    # own properties
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lon = db.Column(db.Numeric(scale=4, asdecimal=True), nullable=False)
    lat = db.Column(db.Numeric(scale=4, asdecimal=True), nullable=False)

    @hybrid_property  # read-only
    def rating(self):
        visits = list(filter(lambda visit: visit.rating is not None, self.visits))

        if not visits:
            return 0.0

        return sum(map(lambda visit: visit.rating, visits)) / len(visits)

    # foreign keys
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # relationships
    owner = db.relationship("User", uselist=False, back_populates="owned_caches")
    visits = db.relationship("CacheVisit", uselist=True, back_populates="cache")
    comments = db.relationship("CacheComment", uselist=True, back_populates="cache")
