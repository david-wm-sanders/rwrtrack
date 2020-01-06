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
