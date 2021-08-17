from datetime import datetime

from everycache_api.extensions import db


class Token(db.Model):
    __tablename__ = "tokens"

    id_ = db.Column("id", db.Integer, primary_key=True)  # avoids shadowing builtin "id"
    jti = db.Column(db.String(36), nullable=False, unique=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    expires = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    revoked = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship("User", uselist=False)
