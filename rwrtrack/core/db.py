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

# Configure blacklist for troublesome usernames
username_blacklist = set()
username_blacklist.add("RAIOORIGINAL")


def get_account_from_db(username):
    return sesh.query(Account).filter_by(username=username).one()


def update_db_from_stats(stats, d):
    account_usernames = set()
    usernames = sesh.query(Account.username).all()
    for u in usernames:
        account_usernames.add(u[0])
    for s in stats:
        # If username in blacklist, skip...
        if s.username in username_blacklist:
            continue
        if s.username not in account_usernames:
            account_usernames.add(s.username)
            # Create a new Account for the username
            account = Account(username=s.username,
                              first_date=d, latest_date=d)
            sesh.add(account)
            # Need to flush so that account._id is populated
            sesh.flush()
        else:
            # Update Account for the username
            account = sesh.query(Account._id) \
                        .filter_by(username=s.username).one()
            sesh.query(Account).filter_by(_id=account._id).update(
                {"latest_date": d})
        # Create a history entry for this stat record
        record = Record(date=d, account_id=account._id,
                        username=s.username, xp=s.xp,
                        time_played=s.time_played,
                        kills=s.kills, deaths=s.deaths,
                        score=s.score, kdr=s.kdr,
                        kill_streak=s.kill_streak,
                        targets_destroyed=s.targets_destroyed,
                        vehicles_destroyed=s.vehicles_destroyed,
                        soldiers_healed=s.soldiers_healed,
                        team_kills=s.team_kills,
                        distance_moved=s.distance_moved,
                        shots_fired=s.shots_fired,
                        throwables_thrown=s.throwables_thrown)
        sesh.add(record)
