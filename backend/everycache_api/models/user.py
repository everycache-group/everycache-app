from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from everycache_api.extensions import db, pwd_context


class User(db.Model):
    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    _password = db.Column("password", db.String(256), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

    auth_tokens = db.relationship("AuthToken", uselist=True, back_populates="user")
    owned_caches = db.relationship("Cache", uselist=True, back_populates="owner")
    cache_visits = db.relationship("CacheVisit", uselist=True, back_populates="user")
    cache_comments = db.relationship(
        "CacheComment", uselist=True, back_populates="author"
    )

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password: str):
        self._password = pwd_context.hash(new_password)

    def verify_password(self, password: str):
        return pwd_context.verify(password, self._password)
