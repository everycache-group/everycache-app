from datetime import datetime, timedelta

from sqlalchemy.orm.session import Session

from database.connection import DBSession, recreate_db_schema
from database.models import Cache, CacheComment, CacheVisit, User


def populate():
    recreate_db_schema()

    db_session: Session = DBSession()

    user1 = User(id_=1, login="user1", name="John Doe")
    user2 = User(id_=2, login="user2", name="Adam Bogdan Nowak")

    db_session.merge(user1)
    db_session.merge(user2)

    db_session.commit()

    cache1 = Cache(
        id_=1,
        owner=user1,
        name="my first cache",
        lon=1.999,
        lat=2.001,
        created_at=datetime.now() - timedelta(days=5),
    )
    cache2 = Cache(
        id_=2,
        owner=user2,
        name="best cache",
        lon=3.14,
        lat=123,
        created_at=datetime.now() - timedelta(hours=1),
    )

    db_session.merge(cache1)
    db_session.merge(cache2)

    db_session.commit()
