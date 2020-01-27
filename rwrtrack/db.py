import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


logger = logging.getLogger(__name__)

DeclarativeBase = declarative_base()
engine = create_engine("sqlite:///rwrtrack_history.db")
# Need to set a logging level here to get sqlalchemy to allow changes to the logging level in logging.py - bizarre!
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
db_session = sessionmaker(bind=engine)
sesh = db_session()

from .dbinfo import DbInfo
from .account import Account
from .record import Record
DeclarativeBase.metadata.create_all(engine)


def _set_db_readonly():
    logger.debug("[Set database query_only ON]")
    sesh.execute("PRAGMA query_only = ON;")


def _set_db_writable():
    logger.debug("[Set database query_only OFF]")
    sesh.execute("PRAGMA query_only = OFF;")


# Make the db readonly by default
_set_db_readonly()
