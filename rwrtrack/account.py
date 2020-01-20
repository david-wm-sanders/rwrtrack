from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound

from .db import DeclarativeBase, sesh
from .exceptions import NoAccountError, NoRecordError


class Account(DeclarativeBase):
    __tablename__ = "accounts"
    _id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    first_date = Column(Integer, nullable=False)
    latest_date = Column(Integer, nullable=False)
    history = relationship("Record", lazy="dynamic")

    def __init__(self, username, date):
        self.username = username
        self.first_date = date
        self.latest_date = date

    def __repr__(self):
        return f"Account(id={self._id}, username='{self.username}', " \
               f"first_date={self.first_date}, latest_date={self.latest_date})"

    @property
    def complete_history(self):
        return self.history.all()

    @property
    def first_record(self):
        return self.history.filter_by(date=self.first_date).one()

    @property
    def latest_record(self):
        return self.history.filter_by(date=self.latest_date).one()

    def on_date(self, date):
        try:
            return self.history.filter_by(date=date).one()
        except NoResultFound as e:
            raise NoRecordError(f"No record for '{self.username}' on {date}") from e


def get_account_by_name(username):
    try:
        return sesh.query(Account).filter_by(username=username).one()
    except NoResultFound as e:
        raise NoAccountError(f"'{username}' not found in database") from e
