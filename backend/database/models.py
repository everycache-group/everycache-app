from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import DetachedInstanceError

from passwords import generate_hash, verify_password


class BaseMixin(object):
    def __repr__(self):
        fields = list()
        for key in vars(self):
            if not key.startswith("_"):
                try:
                    value = repr(getattr(self, key))
                except DetachedInstanceError:
                    value = "DetachedInstanceError"
                finally:
                    fields.append(f"{key.rstrip('_')}={value}")
        output = ",".join(fields)
        return f"{self.__class__.__name__}({output})"

    def to_dict(self):
        output = {}
        for key in vars(self):
            if not key.startswith("_"):
                try:
                    output[key.rstrip("_")] = str(getattr(self, key))
                except DetachedInstanceError:
                    pass
        return output


BaseModel = declarative_base(cls=BaseMixin)


class User(BaseModel):
    __tablename__ = "users"

    __id = Column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    __login = Column("login", String(32), unique=True, nullable=False)
    __password = Column("password", String, nullable=False)
    __email = Column("email", String(128), nullable=True)
    name = Column(String(128), nullable=False)  # first, second, last name in one string

    owned_caches = relationship("Cache", uselist=True, back_populates="owner")
    cache_visits = relationship("CacheVisit", uselist=True, back_populates="user")
    cache_comments = relationship("CacheComment", uselist=True, back_populates="author")

    def __init__(self, id_: int, login: str, password: str, name: str):
        self.__id = id_
        self.__login = login
        self.__password = generate_hash(password)
        self.__name = name

    def verify_password(self, password: str):
        return verify_password(password, self.__password)


class Cache(BaseModel):
    __tablename__ = "caches"

    # class field: "id_", db column: "id"
    id_ = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    lon = Column(Numeric(scale=4, asdecimal=True), nullable=False)
    lat = Column(Numeric(scale=4, asdecimal=True), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)

    owner = relationship("User", uselist=False, back_populates="owned_caches")
    visits = relationship("CacheVisit", uselist=True, back_populates="cache")
    comments = relationship("CacheComment", uselist=True, back_populates="cache")


class CacheVisit(BaseModel):
    __tablename__ = "cache_visits"

    cache_id = Column(Integer, ForeignKey("caches.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    # class field: "datetime_", db column: "datetime"
    datetime_ = Column("datetime", DateTime, nullable=False)
    rating = Column(Integer, nullable=True)

    cache = relationship("Cache", uselist=False, back_populates="visits")
    user = relationship("User", uselist=False, back_populates="cache_visits")

    @classmethod
    def new(cls, cache: Cache, user: User, datetime_: Optional[datetime] = None):
        if not datetime_:
            datetime_ = datetime.utcnow()
        return cls(cache=cache, user=user, datetime_=datetime_)


class CacheComment(BaseModel):
    __tablename__ = "cache_comments"

    cache_id = Column(Integer, ForeignKey("caches.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)

    cache = relationship("Cache", uselist=False, back_populates="comments")
    author = relationship("User", uselist=False, back_populates="cache_comments")

    @classmethod
    def new(
        cls, cache: Cache, user: User, text: str, created_at: Optional[datetime] = None
    ):
        if not created_at:
            created_at = datetime.utcnow()
        return cls(cache=cache, user=user, text=text, created_at=created_at)
