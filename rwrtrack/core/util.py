import logging
from datetime import datetime, timedelta

from sqlalchemy import and_, text
from sqlalchemy.orm import aliased
from sqlalchemy.orm.exc import NoResultFound # as SQLNoResultFound

from .db import DbInfo, sesh
from .account import Account
from .record import Record


logger = logging.getLogger(__name__)
# Configure blacklist for troublesome usernames
username_blacklist = set()
username_blacklist.add("RAIOORIGINAL")
# Set aliases for Record to use in self-join scenarios
RecordA, RecordB = aliased(Record, name="a"), aliased(Record, name="b")


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


def difference(date_older, date_newer, username=None):
    logger.debug(f"Differencing DB for {date_older}-{date_newer}")
    # Shorthands
    ra, rb = RecordA, RecordB
    q = sesh.query(RecordA, RecordB). \
            with_entities(
                ra.account_id.label("account_id"), ra.username.label("username"),
                (ra.xp - rb.xp).label("xp"),
                (ra.time_played - rb.time_played).label("time_played"),
                (ra.kills - rb.kills).label("kills"),
                (ra.deaths - rb.deaths).label("deaths"),
                (ra.kill_streak - rb.kill_streak).label("kill_streak"),
                (ra.targets_destroyed - rb.targets_destroyed).label("targets_destroyed"),
                (ra.vehicles_destroyed - rb.vehicles_destroyed).label("vehicles_destroyed"),
                (ra.soldiers_healed - rb.soldiers_healed).label("soldiers_healed"),
                (ra.team_kills - rb.team_kills).label("team_kills"),
                (ra.distance_moved - rb.distance_moved).label("distance_moved"),
                (ra.shots_fired - rb.shots_fired).label("shots_fired"))
    if username:
        return q.filter(and_(ra.username==username, ra.date==date_newer, rb.date==date_older, ra.account_id==rb.account_id))
    else:
        return q.filter(and_(ra.date==date_newer, rb.date==date_older, ra.account_id==rb.account_id))


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
