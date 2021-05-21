from datetime import datetime

from everycache_api.extensions import db


class CacheComment(db.Model):
    __tablename__ = "cache_comments"

    cache_id = db.Column(db.Integer, db.ForeignKey("caches.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    text = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    cache = db.relationship("Cache", uselist=False, back_populates="comments")
    author = db.relationship("User", uselist=False, back_populates="cache_comments")
