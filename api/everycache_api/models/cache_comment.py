from datetime import datetime

from everycache_api.extensions import db

from .base import BaseMixin


class CacheComment(BaseMixin, db.Model):
    __tablename__ = "cache_comments"

    # own properties
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)

    # foreign keys
    cache_id = db.Column(db.Integer, db.ForeignKey("caches.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # relationships
    cache = db.relationship("Cache", uselist=False, back_populates="comments")
    author = db.relationship("User", uselist=False, back_populates="cache_comments")
