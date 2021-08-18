from enum import Enum

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils.types.choice import ChoiceType

from everycache_api.extensions import db, pwd_context


class User(db.Model):
    class Role(Enum):
        admin = "admin"
        default = "default"

    __tablename__ = "users"

    id_ = db.Column("id", db.Integer, primary_key=True)  # avoids shadowing builtin "id"
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    role = db.Column(
        ChoiceType(Role),
        nullable=False,
        default=Role.default.value,
    )

    owned_caches = db.relationship("Cache", uselist=True, back_populates="owner")
    cache_visits = db.relationship("CacheVisit", uselist=True, back_populates="user")
    cache_comments = db.relationship(
        "CacheComment", uselist=True, back_populates="author"
    )

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = pwd_context.hash(value)

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password)

    def __str__(self):
        return f"<User {self.username}>"
