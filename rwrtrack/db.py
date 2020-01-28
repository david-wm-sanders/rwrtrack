import logging
import types

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


logger = logging.getLogger(__name__)

DeclarativeBase = declarative_base()
engine = create_engine("sqlite:///rwrtrack_history.db")

# Set the sqlalchemy.engine logging level to INFO to get statement and parameter readouts
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
# Define a replacement method for engine.logger.info that modifies the logging level to DEBUG
def _patch_info_log(self, msg, *args, **kwargs):
    if args:
        # If engine.logger.info has non-empty/non-False args, assume it is a parameter call and emit customised msg
        self.logger._log(logging.DEBUG, f"Query parameters: '{msg}'", args, **kwargs)
    else:
        self.logger._log(logging.DEBUG, f"Query: '{msg}'", args, **kwargs)
# Bind the replacement method over the existing method
engine.logger.info = types.MethodType(_patch_info_log, engine)

# Make a session available as sesh
db_session = sessionmaker(bind=engine)
sesh = db_session()

# Late import classes that will have used DeclarativeBase to exist so that create_all works
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
