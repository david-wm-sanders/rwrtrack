from .derivedstats import DerivedStatsMixin


class StatsDiff(DerivedStatsMixin):
    def __init__(self, dates, account_id, username, xp, time_played,
                 kills, deaths, score, kdr, kill_streak,
                 targets_destroyed, vehicles_destroyed, soldiers_healed,
                 team_kills, distance_moved, shots_fired, throwables_thrown):
        self.dates = dates
        self.account_id = account_id
        self.username = username
        self.xp = xp
        self.time_played = time_played
        self.kills = kills
        self.deaths = deaths
        self.score = score
        self.kdr = kdr
        self.kill_streak = kill_streak
        self.targets_destroyed = targets_destroyed
        self.vehicles_destroyed = vehicles_destroyed
        self.soldiers_healed = soldiers_healed
        self.team_kills = team_kills
        self.distance_moved = distance_moved
        self.shots_fired = shots_fired
        self.throwables_thrown = throwables_thrown

    # TODO: Add __repr__
