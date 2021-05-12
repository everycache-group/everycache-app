from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings
from database.models import BaseModel

engine = create_engine(settings.DB_CONNECTION_URI)
DBSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def recreate_db_schema():
    BaseModel.metadata.create_all(bind=engine, checkfirst=True)

    db_session = DBSession()

    pass

    db_session.commit()
    return True
