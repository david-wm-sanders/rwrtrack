import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


logger = logging.getLogger(__name__)

echo = False
DeclarativeBase = declarative_base()
engine = create_engine("sqlite:///rwrtrack_history.db", echo=echo)
DeclarativeBase.metadata.create_all(engine)
db_session = sessionmaker(bind=engine)
sesh = db_session()


def _set_db_readonly():
    # TODO: Make logger.debugs
    # print("[Set db query_only ON]")
    sesh.execute("PRAGMA query_only = ON;")


def _set_db_writable():
    # print("[Set db query_only OFF]")
    sesh.execute("PRAGMA query_only = OFF;")


# Make the db readonly by default
_set_db_readonly()
