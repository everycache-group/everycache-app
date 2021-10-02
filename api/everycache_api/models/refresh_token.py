from datetime import datetime

from everycache_api.extensions import db


class RefreshToken(db.Model):
    __tablename__ = "tokens"

    # base properties
    id_ = db.Column("id", db.Integer, primary_key=True)

    # own properties
    jti = db.Column(db.String(36), nullable=False, unique=True)
    expires = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    revoked = db.Column(db.Boolean, nullable=False, default=False)

    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # relationships
    user = db.relationship("User", uselist=False)
