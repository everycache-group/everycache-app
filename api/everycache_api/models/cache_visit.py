from datetime import datetime

from everycache_api.extensions import db

from .base import BaseMixin


class CacheVisit(BaseMixin, db.Model):
    __tablename__ = "cache_visits"

    # own properties
    visited_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=True)

    # foreign keys
    cache_id = db.Column(db.Integer, db.ForeignKey("caches.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # relationships
    cache = db.relationship("Cache", uselist=False, back_populates="visits")
    user = db.relationship("User", uselist=False, back_populates="cache_visits")
