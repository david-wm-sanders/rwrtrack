from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .db_base import Base


class Account(Base):
    __tablename__ = "accounts"
    _id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    first_date = Column(Integer, nullable=False)
    latest_date = Column(Integer, nullable=False)
    _history = relationship("Record", lazy="dynamic")

    def __repr__(self):
        return f"Account(id={self._id}, " \
               f"username='{self.username}', " \
               f"first_date={self.first_date}, " \
               f"latest_date={self.latest_date})"

    @property
    def history(self):
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
            # print(kwargs)
            latest_date = str(self.latest_date)
            d = datetime.strptime(str(date), "%Y%m%d").date()
            d = d + timedelta(**kwargs)
            d = int(d.strftime("%Y%m%d"))
            return self._history.filter_by(date=d).one()
