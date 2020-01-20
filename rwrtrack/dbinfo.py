import logging

from sqlalchemy import Column, Integer
from sqlalchemy.orm.exc import NoResultFound

from .db import DeclarativeBase, sesh


logger = logging.getLogger(__name__)


class DbInfo(DeclarativeBase):
    __tablename__ = "_dbinfo"
    _id = Column(Integer, primary_key=True)
    first_date = Column(Integer, nullable=False)
    latest_date = Column(Integer, nullable=False)

    def __init__(self, date):
        self.first_date = date
        self.latest_date = date

    def __repr__(self):
        return f"DbInfo(first_date={self.first_date}, latest_date={self.latest_date})"


def get_dbinfo():
    try:
        return sesh.query(DbInfo).one()
    except NoResultFound:
        logger.warning("No row in _dbinfo table, database appears to be blank")
        raise
