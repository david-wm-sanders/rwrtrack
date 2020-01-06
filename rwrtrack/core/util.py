import logging
from datetime import datetime, timedelta

from sqlalchemy import and_, text
from sqlalchemy.orm import aliased
from sqlalchemy.orm.exc import NoResultFound # as SQLNoResultFound

from .db import sesh
from .dbinfo import DbInfo
from .account import Account
from .record import Record


logger = logging.getLogger(__name__)

# Configure blacklist for troublesome usernames
username_blacklist = set()
username_blacklist.add("RAIOORIGINAL")
# Set aliases for Record to use in self-join scenarios
RA, RB = aliased(Record, name="ra"), aliased(Record, name="rb")


class Diff:
    # Columned statistics
    xp = (RA.xp - RB.xp).label("xp")
    time_played = (RA.time_played - RB.time_played).label("time_played")
    kills = (RA.kills - RB.kills).label("kills")
    deaths = (RA.deaths - RB.deaths).label("deaths")
    kill_streak = (RA.kill_streak - RB.kill_streak).label("kill_streak")
    targets_destroyed = (RA.targets_destroyed - RB.targets_destroyed).label("targets_destroyed")
    vehicles_destroyed = (RA.vehicles_destroyed - RB.vehicles_destroyed).label("vehicles_destroyed")
    soldiers_healed = (RA.soldiers_healed - RB.soldiers_healed).label("soldiers_healed")
    team_kills = (RA.team_kills - RB.team_kills).label("team_kills")
    distance_moved = (RA.distance_moved - RB.distance_moved).label("distance_moved")
    shots_fired = (RA.shots_fired - RB.shots_fired).label("shots_fired")
    throwables_thrown = (RA.throwables_thrown - RB.throwables_thrown).label("throwables_thrown")


def get_dbinfo():
    try:
        return sesh.query(DbInfo).one()
    except NoResultFound:
        logger.warn("No row in _dbinfo table, database appears to be blank")
        raise


def get_account_by_name(username):
    return sesh.query(Account).filter_by(username=username).one()


def get_records_on_date(date, **kwargs):
    if not kwargs:
        return sesh.query(Record).filter_by(date=date).all()
    else:
        d = datetime.strptime(str(date), "%Y%m%d").date()
        d = d + timedelta(**kwargs)
        d = int(d.strftime("%Y%m%d"))
        return sesh.query(Record).filter_by(date=d).all()


def difference(date_a, date_b, username=None):
    # logger.debug(f"Differencing DB for {date_b}-{date_a}")
    q = sesh.query(RA.account_id.label("account_id"), RA.username.label("username"),
                    Diff.xp, Diff.time_played, Diff.kills, Diff.deaths, Diff.kill_streak,
                    Diff.targets_destroyed, Diff.vehicles_destroyed, Diff.soldiers_healed,
                    Diff.team_kills, Diff.distance_moved, Diff.shots_fired, Diff.throwables_thrown)
    if username:
        return q.filter(and_(RA.username==username, RA.date==date_a, RB.date==date_b, RA.account_id==RB.account_id))
    else:
        return q.filter(and_(RA.date==date_a, RB.date==date_b, RA.account_id==RB.account_id))


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
            account = Account(username=s.username, date=d)
            sesh.add(account)
            # Need to flush so that account._id is populated
            sesh.flush()
        else:
            # Update Account for the username
            account = sesh.query(Account).filter_by(username=s.username).one()
            account.latest_date = d
        # Create a history entry for this stat record
        record = Record(date=d, account_id=account._id,
                        username=s.username, xp=s.xp,
                        time_played=s.time_played,
                        kills=s.kills, deaths=s.deaths,
                        kill_streak=s.kill_streak,
                        targets_destroyed=s.targets_destroyed,
                        vehicles_destroyed=s.vehicles_destroyed,
                        soldiers_healed=s.soldiers_healed,
                        team_kills=s.team_kills,
                        distance_moved=s.distance_moved,
                        shots_fired=s.shots_fired,
                        throwables_thrown=s.throwables_thrown)
        sesh.add(record)
