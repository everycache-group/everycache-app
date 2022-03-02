import uuid
from enum import Enum

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import ChoiceType, UUIDType

from everycache_api.extensions import db, pwd_context

from .base import BaseMixin


class User(BaseMixin, db.Model):
    class Role(Enum):
        Admin = "admin"
        Default = "default"

    __tablename__ = "users"

    # own properties
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    role = db.Column(
        ChoiceType(Role),
        nullable=False,
        default=Role.Default.value,
    )
    verified = db.Column(db.Boolean, nullable=False, default=False)
    verification_token = db.Column(UUIDType(binary=False), default=uuid.uuid4)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = pwd_context.hash(value)

    # relationships
    owned_caches = db.relationship("Cache", uselist=True, back_populates="owner")
    cache_visits = db.relationship("CacheVisit", uselist=True, back_populates="user")
    cache_comments = db.relationship(
        "CacheComment", uselist=True, back_populates="author"
    )

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password)
