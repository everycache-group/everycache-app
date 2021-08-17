from datetime import datetime

from everycache_api.extensions import db


class CacheComment(db.Model):
    __tablename__ = "cache_comments"

    # avoid shadowing builtin "id"
    id_ = db.Column("id", db.Integer, primary_key=True)
    cache_id = db.Column(db.Integer, db.ForeignKey("caches.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)

    cache = db.relationship("Cache", uselist=False, back_populates="comments")
    author = db.relationship("User", uselist=False, back_populates="cache_comments")
