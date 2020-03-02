from sqlalchemy.sql import func, and_
from sqlalchemy.orm.query import Query

from .db import sesh
from .record import Record, RA, RB
from .difference import Diff
from .filter import filter_
from .constants import EARTH_EQUAT_CIRC


class Avg:
    _count = func.count(Record.account_id).label("_count")
    # Columned statistics
    xp = func.avg(Record.xp).label("xp")
    time_played = func.avg(Record.time_played).label("time_played")
    kills = func.avg(Record.kills).label("kills")
    deaths = func.avg(Record.deaths).label("deaths")
    kill_streak = func.avg(Record.kill_streak).label("kill_streak")
    targets_destroyed = func.avg(Record.targets_destroyed).label("targets_destroyed")
    vehicles_destroyed = func.avg(Record.vehicles_destroyed).label("vehicles_destroyed")
    soldiers_healed = func.avg(Record.soldiers_healed).label("soldiers_healed")
    team_kills = func.avg(Record.team_kills).label("team_kills")
    distance_moved = func.avg(Record.distance_moved).label("distance_moved")
    shots_fired = func.avg(Record.shots_fired).label("shots_fired")
    throwables_thrown = func.avg(Record.throwables_thrown).label("throwables_thrown")

    # Converted statistics
    time_played_hours = (time_played / 60.0).label("time_played_hours")
    distance_moved_km = (distance_moved / 1000.0).label("distance_moved_km")

    # Derived statistics
    score = (kills - deaths).label("score")
    runs_around_the_equator = (distance_moved_km / EARTH_EQUAT_CIRC).label("runs_around_the_equator")


class DiffAvg:
    _count = func.count(RA.account_id).label("_count")
    # Columned statistics
    xp = func.avg(Diff.xp).label("xp")
    time_played = func.avg(Diff.time_played).label("time_played")
    kills = func.avg(Diff.kills).label("kills")
    deaths = func.avg(Diff.deaths).label("deaths")
    kill_streak = func.avg(Diff.kill_streak).label("kill_streak")
    targets_destroyed = func.avg(Diff.targets_destroyed).label("targets_destroyed")
    vehicles_destroyed = func.avg(Diff.vehicles_destroyed).label("vehicles_destroyed")
    soldiers_healed = func.avg(Diff.soldiers_healed).label("soldiers_healed")
    team_kills = func.avg(Diff.team_kills).label("team_kills")
    distance_moved = func.avg(Diff.distance_moved).label("distance_moved")
    shots_fired = func.avg(Diff.shots_fired).label("shots_fired")
    throwables_thrown = func.avg(Diff.throwables_thrown).label("throwables_thrown")

    # Converted statistics
    time_played_hours = (time_played / 60.0).label("time_played_hours")
    distance_moved_km = (distance_moved / 1000.0).label("distance_moved_km")

    # Derived statistics
    score = (kills - deaths).label("score")
    runs_around_the_equator = (distance_moved_km / EARTH_EQUAT_CIRC).label("runs_around_the_equator")


avg_query = Query([Avg._count, Avg.xp, Avg.time_played, Avg.time_played_hours, Avg.kills, Avg.deaths, Avg.score,
                   Avg.kill_streak, Avg.targets_destroyed, Avg.vehicles_destroyed, Avg.soldiers_healed,
                   Avg.team_kills, Avg.distance_moved, Avg.distance_moved_km,
                   Avg.shots_fired, Avg.throwables_thrown, Avg.runs_around_the_equator])

diffavg_query = Query([DiffAvg._count, DiffAvg.xp, DiffAvg.time_played, DiffAvg.time_played_hours,
                       DiffAvg.kills, DiffAvg.deaths, DiffAvg.score, DiffAvg.kill_streak,
                       DiffAvg.targets_destroyed, DiffAvg.vehicles_destroyed, DiffAvg.soldiers_healed,
                       DiffAvg.team_kills, DiffAvg.distance_moved, DiffAvg.distance_moved_km,
                       DiffAvg.shots_fired, DiffAvg.throwables_thrown, DiffAvg.runs_around_the_equator]).\
                       filter(RA.account_id == RB.account_id)


def _avg(date, usernames=None, record_filters=None):
    q = avg_query.with_session(sesh).filter(Record.date == date)
    if usernames:
        q = q.filter(Record.username.in_(usernames))
    if record_filters:
        q = filter_(q, Record, record_filters)
    return q


def avg(date, usernames=None, record_filters=None):
    return _avg(date, usernames, record_filters).one()._asdict()


def _diffavg(date_a, date_b, usernames=None, record_filters=None, diff_filters=None):
    q = diffavg_query.with_session(sesh).filter(RA.date == date_a, RB.date == date_b)
    if usernames:
        q = q.filter(RA.username.in_(usernames))
    if record_filters:
        q = filter_(q, RA, record_filters)
    if diff_filters:
        q = filter_(q, Diff, diff_filters)
    return q


def diffavg(date_a, date_b, usernames=None, record_filters=None, diff_filters=None):
    return _diffavg(date_a, date_b, usernames, record_filters, diff_filters).one()._asdict()
