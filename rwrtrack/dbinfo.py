"""Defines the SQLAlchemy ORM model for the _dbinfo metadata table."""
import logging

from sqlalchemy import Column, Integer
from sqlalchemy.orm.exc import NoResultFound

from .db import DeclarativeBase, sesh


logger = logging.getLogger(__name__)


class DbInfo(DeclarativeBase):
    """Defines the SQLAlchemy ORM model for the DbInfo metadata table."""

    __tablename__ = "_dbinfo"
    _id = Column(Integer, primary_key=True)
    first_date = Column(Integer, nullable=False)
    latest_date = Column(Integer, nullable=False)

    def __init__(self, date):
        """Instantiate a new DbInfo from a date."""
        self.first_date = date
        self.latest_date = date

    def __repr__(self):
        """Return a representation of the DbInfo."""
        return f"DbInfo(first_date={self.first_date}, latest_date={self.latest_date})"


def get_dbinfo(error=True):
    """Get the DbInfo entry from the _dbinfo metadata table."""
    try:
        return sesh.query(DbInfo).one()
    except NoResultFound:
        if error:
            logger.warning("No entry _dbinfo table, database appears to be blank")
            raise
        else:
            return None
