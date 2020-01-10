from sqlalchemy.sql import func, and_
from sqlalchemy.orm.query import Query

from .db import sesh
from .record import Record, RA, RB
from .difference import Diff
from .constants import EARTH_EQUAT_CIRC


class Sum:
    _count = func.count(Record.account_id).label("_count")
    # Columned statistics
    xp = func.sum(Record.xp).label("xp")
    time_played = func.sum(Record.time_played).label("time_played")
    kills = func.sum(Record.kills).label("kills")
    deaths = func.sum(Record.deaths).label("deaths")
    kill_streak = func.sum(Record.kill_streak).label("kill_streak")
    targets_destroyed = func.sum(Record.targets_destroyed).label("targets_destroyed")
    vehicles_destroyed = func.sum(Record.vehicles_destroyed).label("vehicles_destroyed")
    soldiers_healed = func.sum(Record.soldiers_healed).label("soldiers_healed")
    team_kills = func.sum(Record.team_kills).label("team_kills")
    distance_moved = func.sum(Record.distance_moved).label("distance_moved")
    shots_fired = func.sum(Record.shots_fired).label("shots_fired")
    throwables_thrown = func.sum(Record.throwables_thrown).label("throwables_thrown")

    # Converted statistics
    time_played_hours = (time_played / 60.0).label("time_played_hours")
    distance_moved_km = (distance_moved / 1000.0).label("distance_moved_km")

    # Derived statistics
    score = (kills - deaths).label("score")
    runs_around_the_equator = (distance_moved_km / EARTH_EQUAT_CIRC).label("runs_around_the_equator")


class DiffSum:
    _count = func.count(RA.account_id).label("_count")
    # Columned statistics
    xp = func.sum(Diff.xp).label("xp")
    time_played = func.sum(Diff.time_played).label("time_played")
    kills = func.sum(Diff.kills).label("kills")
    deaths = func.sum(Diff.deaths).label("deaths")
    kill_streak = func.sum(Diff.kill_streak).label("kill_streak")
    targets_destroyed = func.sum(Diff.targets_destroyed).label("targets_destroyed")
    vehicles_destroyed = func.sum(Diff.vehicles_destroyed).label("vehicles_destroyed")
    soldiers_healed = func.sum(Diff.soldiers_healed).label("soldiers_healed")
    team_kills = func.sum(Diff.team_kills).label("team_kills")
    distance_moved = func.sum(Diff.distance_moved).label("distance_moved")
    shots_fired = func.sum(Diff.shots_fired).label("shots_fired")
    throwables_thrown = func.sum(Diff.throwables_thrown).label("throwables_thrown")

    # Converted statistics
    time_played_hours = (time_played / 60.0).label("time_played_hours")
    distance_moved_km = (distance_moved / 1000.0).label("distance_moved_km")

    # Derived statistics
    score = (kills - deaths).label("score")
    runs_around_the_equator = (distance_moved_km / EARTH_EQUAT_CIRC).label("runs_around_the_equator")


sum_query = Query([Sum._count, Sum.xp, Sum.time_played, Sum.time_played_hours, Sum.kills, Sum.deaths, Sum.score,
                   Sum.kill_streak, Sum.targets_destroyed, Sum.vehicles_destroyed, Sum.soldiers_healed,
                   Sum.team_kills, Sum.distance_moved, Sum.distance_moved_km,
                   Sum.shots_fired, Sum.throwables_thrown, Sum.runs_around_the_equator])

diffsum_query = Query([DiffSum._count, DiffSum.xp, DiffSum.time_played, DiffSum.time_played_hours,
                       DiffSum.kills, DiffSum.deaths, DiffSum.score, DiffSum.kill_streak,
                       DiffSum.targets_destroyed, DiffSum.vehicles_destroyed, DiffSum.soldiers_healed,
                       DiffSum.team_kills, DiffSum.distance_moved, DiffSum.distance_moved_km,
                       DiffSum.shots_fired, DiffSum.throwables_thrown, DiffSum.runs_around_the_equator]).\
                       filter(RA.account_id==RB.account_id)


def _sum(date, usernames=None):
    q = sum_query.with_session(sesh).filter(Record.date==date)
    if usernames:
        q = q.filter(Record.username.in_(usernames))
    return q


def sum_(date, usernames=None):
    return _sum(date, usernames).one()._asdict()


def _diffsum(date_a, date_b, usernames=None):
    q = diffsum_query.with_session(sesh).filter(and_(RA.date==date_a, RB.date==date_b))
    if usernames:
        q = q.filter(RA.username.in_(usernames))
    return q


def diffsum(date_a, date_b, usernames=None):
    return _diffsum(date_a, date_b, usernames).one()._asdict()
