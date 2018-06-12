from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .db_base import Base
from .account import Account
from .record import Record


engine = create_engine("sqlite:///rwrtrack_history.db")
# engine = create_engine("sqlite:///rwrtrack_history.db", echo=True)
Base.metadata.create_all(engine)
db_session = sessionmaker(bind=engine)
db = db_session()
