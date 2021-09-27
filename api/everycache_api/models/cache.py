from datetime import datetime

from everycache_api.extensions import db


class Cache(db.Model):
    __tablename__ = "caches"

    # base properties
    id_ = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    # own properties
    name = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lon = db.Column(db.Numeric(scale=4, asdecimal=True), nullable=False)
    lat = db.Column(db.Numeric(scale=4, asdecimal=True), nullable=False)

    # foreign keys
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # relationships
    owner = db.relationship("User", uselist=False, back_populates="owned_caches")
    visits = db.relationship("CacheVisit", uselist=True, back_populates="cache")
    comments = db.relationship("CacheComment", uselist=True, back_populates="cache")
