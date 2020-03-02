"""Provides functionality for calculating the differences between Records."""
from sqlalchemy import Float, and_
from sqlalchemy.sql import cast
from sqlalchemy.orm.query import Query

from .db import sesh
from .constants import EARTH_EQUAT_CIRC
from .record import RA, RB


class Diff:
    """Provides shortcuts for differencing Record metrics for use in SQLAlchemy queries."""

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

    # Converted statistics
    # Divide by floats to ensure the division performed by the db in SQL statements is float division
    # See derivedstats.py for more exposition on why this is necessary
    # With time_played_hours and distance_moved_km as floats, casting isn't necessary for variables derived from them
    time_played_hours = (time_played / 60.0).label("time_played_hours")
    distance_moved_km = (distance_moved / 1000.0).label("distance_moved_km")

    # Derived statistics (expressed in terms of the variables above)
    # Cast where division occurs between two ints to ensure that the underlying db divides properly
    score = (kills - deaths).label("score")
    kdr = (cast(kills, Float) / deaths).label("kdr")
    xp_per_hour = (xp / time_played_hours).label("xp_per_hour")
    kills_per_hour = (kills / time_played_hours).label("kills_per_hour")
    deaths_per_hour = (deaths / time_played_hours).label("deaths_per_hour")
    targets_destroyed_per_hour = (targets_destroyed / time_played_hours).label("targets_destroyed_per_hour")
    vehicles_destroyed_per_hour = (vehicles_destroyed / time_played_hours).label("vehicles_destroyed_per_hour")
    soldiers_healed_per_hour = (soldiers_healed / time_played_hours).label("soldiers_healed_per_hour")
    team_kills_per_hour = (team_kills / time_played_hours).label("team_kills_per_hour")
    distance_moved_km_per_hour = (distance_moved_km / time_played_hours).label("distance_moved_km_per_hour")
    shots_fired_per_hour = (shots_fired / time_played_hours).label("shots_fired_per_hour")
    throwables_thrown_per_hour = (throwables_thrown / time_played_hours).label("throwables_thrown_per_hour")
    kills_per_km_moved = (kills / distance_moved_km).label("kills_per_km_moved")
    xp_per_shot_fired = (cast(xp, Float) / shots_fired).label("xp_per_shot_fired")
    xp_per_kill = (cast(xp, Float) / kills).label("xp_per_kill")
    shots_fired_per_kill = (cast(shots_fired, Float) / kills).label("shots_fired_per_kill")
    team_kills_per_kill = (cast(team_kills, Float) / kills).label("team_kills_per_kill")
    runs_around_the_equator = (distance_moved_km / EARTH_EQUAT_CIRC).label("runs_around_the_equator")

    # Changes in derived statistics
    # _score = (RA.score - RB.score).label("_score")
    _kdr = (RA.kdr - RB.kdr).label("_kdr")
    _xp_per_hour = (RA.xp_per_hour - RB.xp_per_hour).label("_xp_per_hour")
    _kills_per_hour = (RA.kills_per_hour - RB.kills_per_hour).label("_kills_per_hour")
    _deaths_per_hour = (RA.deaths_per_hour - RB.deaths_per_hour).label("_deaths_per_hour")
    _targets_destroyed_per_hour = (RA.targets_destroyed_per_hour - RB.targets_destroyed_per_hour).\
        label("_targets_destroyed_per_hour")
    _vehicles_destroyed_per_hour = (RA.vehicles_destroyed_per_hour - RB.vehicles_destroyed_per_hour).\
        label("_vehicles_destroyed_per_hour")
    _soldiers_healed_per_hour = (RA.soldiers_healed_per_hour - RB.soldiers_healed_per_hour).\
        label("_soldiers_healed_per_hour")
    _team_kills_per_hour = (RA.team_kills_per_hour - RB.team_kills_per_hour).label("_team_kills_per_hour")
    _distance_moved_km_per_hour = (RA.distance_moved_km_per_hour - RB.distance_moved_km_per_hour).\
        label("_distance_moved_km_per_hour")
    _shots_fired_per_hour = (RA.shots_fired_per_hour - RB.shots_fired_per_hour).label("_shots_fired_per_hour")
    _throwables_thrown_per_hour = (RA.throwables_thrown_per_hour - RB.throwables_thrown_per_hour).\
        label("_throwables_thrown_per_hour")
    _kills_per_km_moved = (RA.kills_per_km_moved - RB.kills_per_km_moved).label("_kills_per_km_moved")
    _xp_per_shot_fired = (RA.xp_per_shot_fired - RB.xp_per_shot_fired).label("_xp_per_shot_fired")
    _xp_per_kill = (RA.xp_per_kill - RB.xp_per_kill).label("_xp_per_kill")
    _shots_fired_per_kill = (RA.shots_fired_per_kill - RB.shots_fired_per_kill).label("_shots_fired_per_kill")
    _team_kills_per_kill = (RA.team_kills_per_kill - RB.team_kills_per_kill).label("_team_kills_per_kill")


diff_query = Query([RA.account_id.label("account_id"), RA.username.label("username"),
                    RA.date.label("ra_date"), RB.date.label("rb_date"),
                    Diff.xp, Diff.time_played, Diff.time_played_hours, Diff.kills, Diff.deaths, Diff.score,
                    Diff.kill_streak, Diff.targets_destroyed, Diff.vehicles_destroyed, Diff.soldiers_healed,
                    Diff.team_kills, Diff.distance_moved, Diff.distance_moved_km,
                    Diff.shots_fired, Diff.throwables_thrown,
                    Diff.kdr, Diff._kdr, Diff.xp_per_hour, Diff._xp_per_hour,
                    Diff.kills_per_hour, Diff._kills_per_hour, Diff.deaths_per_hour, Diff._deaths_per_hour,
                    Diff.targets_destroyed_per_hour, Diff._targets_destroyed_per_hour,
                    Diff.vehicles_destroyed_per_hour, Diff._vehicles_destroyed_per_hour,
                    Diff.soldiers_healed_per_hour, Diff._soldiers_healed_per_hour,
                    Diff.team_kills_per_hour, Diff._team_kills_per_hour,
                    Diff.distance_moved_km_per_hour, Diff._distance_moved_km_per_hour,
                    Diff.shots_fired_per_hour, Diff._shots_fired_per_hour,
                    Diff.throwables_thrown_per_hour, Diff._throwables_thrown_per_hour,
                    Diff.kills_per_km_moved, Diff._kills_per_km_moved, Diff.xp_per_shot_fired, Diff._xp_per_shot_fired,
                    Diff.xp_per_kill, Diff._xp_per_kill, Diff.shots_fired_per_kill, Diff._shots_fired_per_kill,
                    Diff.team_kills_per_kill, Diff._team_kills_per_kill, Diff.runs_around_the_equator]).\
                    filter(RA.account_id == RB.account_id)


def difference(date_a, date_b, usernames=None):
    """Return a SQLAlchemy query that will calculate the difference between the Records on date_a and date_b."""
    q = diff_query.with_session(sesh).filter(RA.date == date_a, RB.date == date_b)
    if usernames:
        q = q.filter(RA.username.in_(usernames))
    return q
