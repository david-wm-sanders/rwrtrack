import logging
import time
import types

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


logger = logging.getLogger(__name__)


# Configure query profiling
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    ns_start = time.time_ns()
    conn.info.setdefault('query_start_time', []).append(ns_start)
    logger.debug(f"Starting query: '{statement}'\nwith parameters: '{parameters}'")


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    ns_end = time.time_ns()
    total = ns_end - conn.info['query_start_time'].pop(-1)
    logger.debug(f"Query took: {total / 1_000_000:.2f}ms")


# Declare the base, create the engine, make a session to sesh
DeclarativeBase = declarative_base()
engine = create_engine("sqlite:///rwrtrack_history.db")
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
