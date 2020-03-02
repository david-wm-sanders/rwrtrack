"""Defines the SQLAlchemy ORM model for a RWR player account."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound

from .db import DeclarativeBase, sesh
from .exceptions import NoAccountError, NoRecordError


class Account(DeclarativeBase):
    """Defines the SQLAlchemy ORM model for a RWR player account."""

    __tablename__ = "accounts"
    _id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    first_date = Column(Integer, nullable=False)
    latest_date = Column(Integer, nullable=False)
    records = relationship("Record", lazy="dynamic")

    def __init__(self, username, date):
        """Instantiate a new Account from a username and date."""
        self.username = username
        self.first_date = date
        self.latest_date = date

    def __repr__(self):
        """Return a representation of the Account."""
        return f"Account(id={self._id}, username='{self.username}', " \
               f"first_date={self.first_date}, latest_date={self.latest_date})"

    @property
    def all_records(self):
        """Return all Records associated with the Account as a list."""
        return self.records.all()

    @property
    def first_record(self):
        """Return the first Record associated with the Account."""
        return self.records.filter_by(date=self.first_date).one()

    @property
    def latest_record(self):
        """Return the latest Record associated with the Account."""
        return self.records.filter_by(date=self.latest_date).one()

    def on_date(self, date):
        """Return the Record for the Account on the date."""
        try:
            return self.records.filter_by(date=date).one()
        except NoResultFound as e:
            raise NoRecordError(f"No record for '{self.username}' on {date}") from e


def get_account_by_name(username):
    """Find an Account in the database by username."""
    try:
        return sesh.query(Account).filter_by(username=username).one()
    except NoResultFound as e:
        raise NoAccountError(f"'{username}' not found in database") from e
