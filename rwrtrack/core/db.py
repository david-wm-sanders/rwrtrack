from sqlalchemy import create_engine
from sqlalchemy import Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .db_base import Base
from .account import Account
from .record import Record


class DbInfo(Base):
    __tablename__ = "_dbinfo"
    _id = Column(Integer, primary_key=True)
    first_date = Column(Integer, nullable=False)
    latest_date = Column(Integer, nullable=False)

    def __repr__(self):
        return f"DbInfo(first_date={self.first_date}, " \
               f"latest_date={self.latest_date})"


engine = create_engine("sqlite:///rwrtrack_history.db")
# engine = create_engine("sqlite:///rwrtrack_history.db", echo=True)
Base.metadata.create_all(engine)
db_session = sessionmaker(bind=engine)
sesh = db_session()


def get_account_from_db(username):
    return sesh.query(Account).filter_by(username=username).one()
