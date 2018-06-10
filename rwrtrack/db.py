from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import create_engine, MetaData, \
                       Table, Column, ForeignKey, \
                       Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from stats import load_stats_from_csv


engine = create_engine("sqlite:///rwrtrack_history.db")
# engine = create_engine("sqlite:///rwrtrack_history.db", echo=True)
Base = declarative_base()


class Account(Base):
    __tablename__ = "accounts"
    _id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    xp = Column(Integer, nullable=False)
    time_played = Column(Integer, nullable=False)
    kills = Column(Integer, nullable=False)
    deaths = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    kdr = Column(Float, nullable=False)
    kill_streak = Column(Integer, nullable=False)
    targets_destroyed = Column(Integer, nullable=False)
    vehicles_destroyed = Column(Integer, nullable=False)
    soldiers_healed = Column(Integer, nullable=False)
    team_kills = Column(Integer, nullable=False)
    distance_moved = Column(Integer, nullable=False)
    shots_fired = Column(Integer, nullable=False)
    throwables_thrown = Column(Integer, nullable=False)
    _first_date = Column(Integer, nullable=False)
    _date = Column(Integer, nullable=False)
    _history = relationship("History")


class History(Base):
    __tablename__ = "history"
    date = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts._id"), primary_key=True)
    username = Column(String, nullable=False)
    xp = Column(Integer, nullable=False)
    time_played = Column(Integer, nullable=False)
    kills = Column(Integer, nullable=False)
    deaths = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    kdr = Column(Float, nullable=False)
    kill_streak = Column(Integer, nullable=False)
    targets_destroyed = Column(Integer, nullable=False)
    vehicles_destroyed = Column(Integer, nullable=False)
    soldiers_healed = Column(Integer, nullable=False)
    team_kills = Column(Integer, nullable=False)
    distance_moved = Column(Integer, nullable=False)
    shots_fired = Column(Integer, nullable=False)
    throwables_thrown = Column(Integer, nullable=False)

db_session = sessionmaker(bind=engine)
db = db_session()

if __name__ == '__main__':
    print("Running db.py as __main__ - migrating CSV to database...")

    # Delete the old database
    print("Obliterating the old database (temporary)...")
    db_path = Path(__file__).parent / Path("../rwrtrack_history.db")
    if db_path.exists():
        db_path.unlink()

    # Create a new empty database
    Base.metadata.create_all(engine)

    # Get all CSV files and filter
    print("Finding CSV files for migration...")
    csv_hist_path = Path(__file__).parent / Path("../csv_historical")
    csv_file_paths = sorted(list(csv_hist_path.glob("*.csv")))
    # Filter out CSV files that are not being migrated (for reasons...)
    csv_file_paths = filter(lambda x: "2017" not in x.stem, csv_file_paths)

    # TODO: Fix to load account_usernames from database
    account_usernames = set()
    for csv_file_path in csv_file_paths:
        print(f"Processing file: {csv_file_path.name}...")
        stats = load_stats_from_csv(csv_file_path)
        # Fix dates
        d = datetime.strptime(csv_file_path.stem, "%Y-%m-%d").date()
        d = d - timedelta(days=1)
        d = int(d.strftime("%Y%m%d"))

        # First pass: add/update accounts
        for s in stats:
            if s.username not in account_usernames:
                account_usernames.add(s.username)
                # Create a new Account for the user
                account = Account(username = s.username,
                                  xp = s.xp,
                                  time_played = s.time_played,
                                  kills = s.kills,
                                  deaths = s.deaths,
                                  score = s.score,
                                  kdr = s.kdr,
                                  kill_streak = s.kill_streak,
                                  targets_destroyed = s.targets_destroyed,
                                  vehicles_destroyed = s.vehicles_destroyed,
                                  soldiers_healed = s.soldiers_healed,
                                  team_kills = s.team_kills,
                                  distance_moved = s.distance_moved,
                                  shots_fired = s.shots_fired,
                                  throwables_thrown = s.throwables_thrown,
                                  _first_date = d,
                                  _date = d)
                db.add(account)
            else:
                # TODO: Update Account
                pass
        db.commit()

        # Second pass: add history
        for s in stats:
            account = db.query(Account._id) \
                        .filter_by(username=s.username).one()
            # Create a history entry for this stat record
            history = History(date = d,
                              account_id = account._id,
                              username = s.username,
                              xp = s.xp,
                              time_played = s.time_played,
                              kills = s.kills,
                              deaths = s.deaths,
                              score = s.score,
                              kdr = s.kdr,
                              kill_streak = s.kill_streak,
                              targets_destroyed = s.targets_destroyed,
                              vehicles_destroyed = s.vehicles_destroyed,
                              soldiers_healed = s.soldiers_healed,
                              team_kills = s.team_kills,
                              distance_moved = s.distance_moved,
                              shots_fired = s.shots_fired,
                              throwables_thrown = s.throwables_thrown)
            db.add(history)
        db.commit()
