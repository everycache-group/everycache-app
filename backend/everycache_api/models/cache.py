from datetime import datetime

from everycache_api.extensions import db


class Cache(db.Model):
    __tablename__ = "caches"

    __id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    lon = db.Column(db.Numeric(scale=4, asdecimal=True), nullable=False)
    lat = db.Column(db.Numeric(scale=4, asdecimal=True), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

    owner = db.relationship("User", uselist=False, back_populates="owned_caches")
    visits = db.relationship("CacheVisit", uselist=True, back_populates="cache")
    comments = db.relationship("CacheComment", uselist=True, back_populates="cache")
