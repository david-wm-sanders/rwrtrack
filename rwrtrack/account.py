from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .db_base import Base


class Account(Base):
    __tablename__ = "accounts"
    _id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    first_date = Column(Integer, nullable=False)
    latest_date = Column(Integer, nullable=False)
    history = relationship("Record")

    def __repr__(self):
        return f"Account(id={self._id}, " \
               f"username='{self.username}', " \
               f"first_date={self.first_date}, " \
               f"latest_date={self.latest_date})"

    @property
    def latest_record(self):
        return self.history[-1]
