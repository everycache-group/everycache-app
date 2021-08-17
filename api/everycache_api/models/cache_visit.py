from datetime import datetime

from everycache_api.extensions import db


class CacheVisit(db.Model):
    __tablename__ = "cache_visits"

    cache_id = db.Column(db.Integer, db.ForeignKey("caches.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    visited_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=True)

    cache = db.relationship("Cache", uselist=False, back_populates="visits")
    user = db.relationship("User", uselist=False, back_populates="cache_visits")
