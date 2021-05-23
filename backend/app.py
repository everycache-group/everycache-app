import os
from collections import OrderedDict
from datetime import date, datetime

from flask import Flask, jsonify, render_template, request
from flask_caching import Cache as AppCache
from flask_cors import CORS
from sqlalchemy.orm.exc import NoResultFound

import settings
from database.connection import DBSession, recreate_db_schema
from database.models import Cache, CacheComment, CacheVisit, User
from parse_datetime import (
    DateParseError,
    DateTimeParseError,
    parse_date,
    parse_datetime,
)

config = {
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_TYPE": "SimpleCache",
    "JSON_AS_ASCII": False,
    "JSONIFY_PRETTYPRINT_REGULAR": True,
}
app = Flask(__name__, static_folder="./static", template_folder="./public")
app.config.from_mapping(config)

app_cache = AppCache(app)
CORS(app, origin={settings.FRONTEND_APP_URL})

if settings.DEBUG:

    @app.errorhandler(Exception)
    def handle_bad_request(e):
        return jsonify(error="Unexpected error", reason=str(e)), 400

    @app.route("/")
    @app_cache.cached(timeout=30)
    def sitemap():
        rules = sorted(app.url_map.iter_rules(), key=lambda rule: str(rule.rule))
        endpoints = OrderedDict(
            ((rule.rule, rule.endpoint) for rule in rules if rule.endpoint != "static")
        )

        static_files = sorted(os.listdir("./static"))
        for static_file_path in static_files:
            endpoints[f"/static/{static_file_path}"] = static_file_path

        return render_template("sitemap.html", endpoints=endpoints)


@app.errorhandler(NoResultFound)
def handle_no_results(e):
    return jsonify(error="No data found", reason=str(e)), 400


@app.errorhandler(DateParseError)
def handle_date_parsing_error(e):
    return jsonify(error="Date parsing error", reason=str(e)), 400


@app.errorhandler(DateTimeParseError)
def handle_datetime_parsing_error(e):
    return jsonify(error="Datetime parsing error", reason=str(e)), 400


@app.route("/caches")
def list_caches():
    with DBSession() as db_session:
        caches = db_session.query(Cache).all()
        return {"caches": [cache.to_dict() for cache in caches]}


@app.route("/users")
def list_users():
    with DBSession() as db_session:
        users = db_session.query(User).all()
        return {"users": [user.to_dict() for user in users]}


@app.route("/owner-caches/<int:user_id>")
def list_user_owned_caches(user_id: str):
    with DBSession() as db_session:
        user: User = db_session.query(User).filter_by(id_=user_id).one()
        return {"caches": [cache.to_dict() for cache in user.owned_caches]}
