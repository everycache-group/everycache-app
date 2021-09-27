from datetime import datetime

from everycache_api.extensions import db


class CacheVisit(db.Model):
    __tablename__ = "cache_visits"

    # base properties
    id_ = db.Column("id", db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    # own properties
    visited_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=True)

    # foreign keys
    cache_id = db.Column(db.Integer, db.ForeignKey("caches.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # relationships
    cache = db.relationship("Cache", uselist=False, back_populates="visits")
    user = db.relationship("User", uselist=False, back_populates="cache_visits")
