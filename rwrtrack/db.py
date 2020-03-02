"""Provides core rwrtrack database functionality."""
import logging
import time
import types

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


logger = logging.getLogger(__name__)

# Declare the base, create the engine, make a session to sesh
DeclarativeBase = declarative_base()
engine = create_engine("sqlite:///rwrtrack_history.db")
db_session = sessionmaker(bind=engine)
sesh = db_session()


# Configure query profiling
@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Listen for SQLAlchemy engine before_cursor_execute event to note execution start time."""
    ns_start = time.time_ns()
    conn.info.setdefault('query_start_time', []).append(ns_start)
    logger.debug(f"Executing stmt: '{statement}'\nwith parameters: '{parameters}'")


@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Listen for SQLAlchemy engine after_cursor_execute event to log the time taken for cursor execution."""
    ns_end = time.time_ns()
    total = ns_end - conn.info['query_start_time'].pop(-1)
    logger.debug(f"Execution took: {total / 1_000_000:.2f}ms")


# Late import classes that will have used DeclarativeBase to exist so that create_all works
# Skip E402 (module level import not at top of file) during pycodestyle checks
from .dbinfo import DbInfo  # noqa: E402
from .account import Account  # noqa: E402
from .record import Record  # noqa: E402
DeclarativeBase.metadata.create_all(engine)


def _set_db_readonly():
    """Execute a sqlite PRAGMA statement that makes the database readonly."""
    logger.debug("Make database readonly [query_only ON]")
    sesh.execute("PRAGMA query_only = ON;")


def _set_db_writable():
    """Execute a sqlite PRAGMA statement that makes the database writable."""
    logger.debug("Make database writable [query_only OFF]")
    sesh.execute("PRAGMA query_only = OFF;")


# Make the db readonly by default
_set_db_readonly()
