from everycache_api.extensions import db


class AuthToken(db.Model):
    __tablename__ = "auth_tokens"

    id_ = db.Column("id", db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", uselist=False, back_populates="auth_tokens")
