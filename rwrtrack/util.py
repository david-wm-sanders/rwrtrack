import logging
import time

from .db import sesh
from .account import Account
from .record import Record


logger = logging.getLogger(__name__)

# Configure blacklist for troublesome usernames
username_blacklist = set()
username_blacklist.add("RAIOORIGINAL")


def process_numeric_dates(date_string):
    if date_string.isnumeric():
        return "single", int(date_string)
    else:
        # Handle date ranges
        dates = date_string.split("-")
        d_older = int(dates[0])
        d_newer = int(dates[1])
        if (d_older > d_newer):
            logger.error("Dates must be older-newer!")
            sys.exit(1)
        # return "range", (d_older, d_newer)
        return "range", (d_newer, d_older)


def update_db_from_stats(stats, d):
    t0 = time.time()

    account_usernames = set()
    usernames = sesh.query(Account.username).all()
    for u in usernames:
        account_usernames.add(u[0])

    recs = []
    for s in stats:
        # If username in blacklist, skip...
        if s.username in username_blacklist:
            continue
        if s.username not in account_usernames:
            account_usernames.add(s.username)
            # Create a new Account for the username
            account = Account(username=s.username, date=d)
            sesh.add(account)
            # Need to flush so that account._id is populated
            sesh.flush()
        else:
            # Update Account for the username
            account = sesh.query(Account).filter_by(username=s.username).one()
            account.latest_date = d
        # Create a history entry for this stat record
        rec = dict(date=d, account_id=account._id, username=s.username, xp=s.xp, time_played=s.time_played,
                   kills=s.kills, deaths=s.deaths, kill_streak=s.kill_streak,
                   targets_destroyed=s.targets_destroyed, vehicles_destroyed=s.vehicles_destroyed,
                   soldiers_healed=s.soldiers_healed, team_kills=s.team_kills, distance_moved=s.distance_moved,
                   shots_fired=s.shots_fired, throwables_thrown=s.throwables_thrown)
        recs.append(rec)

    sesh.bulk_insert_mappings(Record, recs)
    sesh.commit()
    logger.info(f"db update for {d} took {(time.time() - t0):.2f} seconds")
