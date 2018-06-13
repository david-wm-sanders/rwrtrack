from .derivedstats import DerivedStatsMixin


class StatsDiff(DerivedStatsMixin):
    def __init__(self, dates, account_ids, usernames, xp, time_played,
                 kills, deaths, score, kdr, kill_streak,
                 targets_destroyed, vehicles_destroyed, soldiers_healed,
                 team_kills, distance_moved, shots_fired, throwables_thrown):
        self.dates = dates
        self.account_ids = account_ids
        self.usernames = usernames
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

    def __repr__(self):
        return f"StatsDiff(dates={self.dates}, " \
               f"account_ids={self.account_ids}, " \
               f"usernames={self.usernames}, " \
               f"xp={self.xp}, time_played={self.time_played}, " \
               f"kills={self.kills}, deaths={self.deaths}, " \
               f"score={self.score}, kdr={self.kdr}, " \
               f"kill_streak={self.kill_streak}, " \
               f"targets_destroyed={self.targets_destroyed}, " \
               f"vehicles_destroyed={self.vehicles_destroyed}, " \
               f"soldiers_healed={self.soldiers_healed}, " \
               f"team_kills={self.team_kills}, " \
               f"distance_moved={self.distance_moved}, " \
               f"shots_fired={self.shots_fired}, " \
               f"throwables_thrown={self.throwables_thrown})"
