import logging
from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .db_base import DeclarativeBase


logger = logging.getLogger(__name__)


class Account(DeclarativeBase):
    __tablename__ = "accounts"
    _id = Column(Integer, primary_key=True)
    _username = Column("username", String, nullable=False, unique=True)
    _first_date = Column("first_date", Integer, nullable=False)
    _latest_date = Column("latest_date", Integer, nullable=False)
    _history = relationship("Record", lazy="dynamic")

    def __init__(self, username, date):
        self._username = username
        self._first_date = date
        self._latest_date = date

    @hybrid_property
    def id_(self):
        return self._id

    @hybrid_property
    def username(self):
        return self._username

    @hybrid_property
    def first_date(self):
        return self._first_date

    @hybrid_property
    def latest_date(self):
        return self._latest_date

    @latest_date.setter
    def latest_date(self, value):
        self._latest_date = value

    @hybrid_property
    def history(self):
        return self._history

    def __repr__(self):
        return f"Account(id={self._id}, " \
               f"username='{self.username}', " \
               f"first_date={self.first_date}, " \
               f"latest_date={self.latest_date})"

    @property
    def complete_history(self):
        return self._history.all()

    @property
    def first_record(self):
        return self._history.filter_by(date=self.first_date).one()

    @property
    def latest_record(self):
        return self._history.filter_by(date=self.latest_date).one()

    def on_date(self, date, **kwargs):
        if not kwargs:
            return self._history.filter_by(date=date).one()
        else:
            d = datetime.strptime(str(date), "%Y%m%d").date()
            d = d + timedelta(**kwargs)
            d = int(d.strftime("%Y%m%d"))
            return self._history.filter_by(date=d).one()
