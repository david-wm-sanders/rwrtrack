from sqlalchemy import Float
from sqlalchemy.sql import cast

from .record import RA, RB


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

    # Converted statistics
    time_played_hours = (time_played / 60.0).label("time_played_hours")
    distance_moved_km = (distance_moved / 1000.0).label("distance_moved_km")

    # Derived statistics (expressed in terms of the variables above)
    # Cast the first variable, where division occurs, to ensure that the underlying db divides properly
    score = (kills - deaths).label("score")
    kdr = (cast(kills, Float) / deaths).label("kdr")
    xp_per_hour = (cast(xp, Float) / time_played_hours).label("xp_per_hour")
    kills_per_hour = (cast(kills, Float) / time_played_hours).label("kills_per_hour")
    deaths_per_hour = (cast(deaths, Float) / time_played_hours).label("deaths_per_hour")
    targets_destroyed_per_hour = (cast(targets_destroyed, Float) / time_played_hours).\
                                    label("targets_destroyed_per_hour")
    vehicles_destroyed_per_hour = (cast(vehicles_destroyed, Float) / time_played_hours).\
                                    label("vehicles_destroyed_per_hour")
    soldiers_healed_per_hour = (cast(soldiers_healed, Float) / time_played_hours).\
                                    label("soldiers_healed_per_hour")
    team_kills_per_hour = (cast(team_kills, Float) / time_played_hours).label("team_kills_per_hour")
    distance_moved_km_per_hour = (cast(distance_moved_km, Float) / time_played_hours).\
                                    label("distance_moved_km_per_hour")
    shots_fired_per_hour = (cast(shots_fired, Float) / time_played_hours).label("shots_fired_per_hour")
    throwables_thrown_per_hour = (cast(throwables_thrown, Float) / time_played_hours).\
                                    label("throwables_thrown_per_hour")

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
