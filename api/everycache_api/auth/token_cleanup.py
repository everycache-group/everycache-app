from datetime import datetime

from apscheduler.triggers.interval import IntervalTrigger
from flask import current_app
from pytz import utc

from everycache_api.extensions import apscheduler, db
from everycache_api.models import Token


def cleanup_expired_tokens():
    with apscheduler.app.app_context():
        tokens = Token.query.filter(Token.expires < datetime.utcnow()).all()

        if tokens:
            current_app.logger.info(
                f"Found {len(tokens)} expired tokens in database. Cleaning up..."
            )

            for token in tokens:
                db.session.delete(token)

            db.session.commit()

            current_app.logger.info("Done")
        else:
            current_app.logger.info("No expired tokens found in database.")


def add_token_cleanup_job():
    # add job to scheduler
    trigger = IntervalTrigger(hour="*/12", timezone=utc)
    apscheduler.add_job("token_cleanup_job", cleanup_expired_tokens, trigger=trigger)
