# Approximate equatorial circumference of Earth
earth_equatorial_circumference = 40075  # km


class DerivedStatsMixin:
    @property
    def time_played_hours(self):
        return self.time_played / 60

    @property
    def distance_moved_km(self):
        return self.distance_moved / 1000

    @property
    def xp_ph(self):
        try:
            return self.xp / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def kills_ph(self):
        try:
            return self.kills / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def deaths_ph(self):
        try:
            return self.deaths / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def targets_destroyed_ph(self):
        try:
            return self.targets_destroyed / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def vehicles_destroyed_ph(self):
        try:
            return self.vehicles_destroyed / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def soldiers_healed_ph(self):
        try:
            return self.soldiers_healed / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def team_kills_ph(self):
        try:
            return self.team_kills / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def distance_moved_km_ph(self):
        try:
            return self.distance_moved_km / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def shots_fired_ph(self):
        try:
            return self.shots_fired / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def throwables_thrown_ph(self):
        try:
            return self.throwables_thrown / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def xp_pk(self):
        try:
            return self.xp / self.kills
        except ZeroDivisionError:
            return 0

    @property
    def xp_pb(self):
        try:
            return self.xp / self.shots_fired
        except ZeroDivisionError:
            return 0

    @property
    def shots_fired_pk(self):
        try:
            return self.shots_fired / self.kills
        except ZeroDivisionError:
            return 0

    @property
    def team_kills_pk(self):
        try:
            return self.team_kills / self.kills
        except ZeroDivisionError:
            return 0

    @property
    def runs_around_the_equator(self):
        return self.distance_moved_km / earth_equatorial_circumference
