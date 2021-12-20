from datetime import datetime, timedelta

from apscheduler.triggers.interval import IntervalTrigger
from flask import current_app
from pytz import utc

from everycache_api.extensions import apscheduler, db
from everycache_api.models import Token


def cleanup_expired_tokens():
    with apscheduler.app.app_context():
        query = Token.query.filter(Token.expires < datetime.utcnow())
        count = query.count()

        if count:
            current_app.logger.info(
                f"Found {count} expired tokens in database. Cleaning up..."
            )

            query.delete()
            db.session.commit()

            current_app.logger.info("Done")
        else:
            current_app.logger.info("No expired tokens found in database.")


def add_token_cleanup_job():
    # add job to scheduler
    trigger = IntervalTrigger(
        hours=12, timezone=utc, start_date=datetime.utcnow() + timedelta(minutes=1)
    )
    apscheduler.add_job(
        "token_cleanup_job",
        cleanup_expired_tokens,
        trigger=trigger,
        misfire_grace_time=60,
        coalesce=True,
    )
