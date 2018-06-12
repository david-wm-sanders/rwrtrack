from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from db_base import Base
from account import Account
from record import Record

from stats import load_stats_from_csv


engine = create_engine("sqlite:///rwrtrack_history.db")
# engine = create_engine("sqlite:///rwrtrack_history.db", echo=True)
db_session = sessionmaker(bind=engine)
db = db_session()

if __name__ == '__main__':
    print("Running db.py as __main__ - migrating CSV to database...")

    # Configure blacklist for troublesome usernames
    username_blacklist = set()
    username_blacklist.add("RAIOORIGINAL")
    # print(username_blacklist)

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

        for s in stats:
            # If username in blacklist, skip...
            if s.username in username_blacklist:
                continue
            if s.username not in account_usernames:
                account_usernames.add(s.username)
                # Create a new Account for the username
                account = Account(username=s.username,
                                  first_date=d, latest_date=d)
                db.add(account)
                # Need to flush so that account._id is populated
                db.flush()
            else:
                account = db.query(Account._id) \
                            .filter_by(username=s.username).one()
                db.query(Account).filter_by(_id=account._id).update(
                    {"latest_date": d})
                # Update Account for the username
                pass

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
            db.add(record)

        db.commit()
