import logging

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base


logger = logging.getLogger(__name__)

DeclarativeBase = declarative_base()
echo = False


class DbInfo(DeclarativeBase):
    __tablename__ = "_dbinfo"
    _id = Column(Integer, primary_key=True)
    _first_date = Column("first_date", Integer, nullable=False)
    _latest_date = Column("latest_date", Integer, nullable=False)

    def __init__(self, date):
        self._first_date = date
        self._latest_date = date

    @hybrid_property
    def first_date(self):
        return self._first_date

    @hybrid_property
    def latest_date(self):
        return self._latest_date

    @latest_date.setter
    def latest_date(self, value):
        self._latest_date = value

    def __repr__(self):
        return f"DbInfo(first_date={self.first_date}, " \
               f"latest_date={self.latest_date})"


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
