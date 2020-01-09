from sqlalchemy.sql import func
from sqlalchemy.orm.query import Query

from .db import sesh
from .record import Record
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
    time_played_hours = (func.sum(Record.time_played) / 60.0).label("time_played_hours")
    distance_moved_km = (func.sum(Record.distance_moved) / 1000.0).label("distance_moved_km")

    # Derived statistics
    score = (kills - deaths).label("score")
    runs_around_the_equator = (distance_moved_km / EARTH_EQUAT_CIRC).label("runs_around_the_equator")


sum_query = Query([Sum._count, Sum.xp, Sum.time_played, Sum.time_played_hours, Sum.kills, Sum.deaths, Sum.score,
                   Sum.kill_streak, Sum.targets_destroyed, Sum.vehicles_destroyed, Sum.soldiers_healed,
                   Sum.team_kills, Sum.distance_moved, Sum.distance_moved_km,
                   Sum.shots_fired, Sum.throwables_thrown, Sum.runs_around_the_equator])


def sum_(date, usernames=None):
    q = sum_query.with_session(sesh).filter(Record.date==date)
    if usernames:
        q = q.filter(Record.username.in_(usernames))
    return q
