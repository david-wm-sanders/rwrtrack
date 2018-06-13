# Approximate equatorial circumference of Earth
earth_equat_circumference = 40075  # km


class DerivedStatsMixin:
    @property
    def time_played_hours(self):
        return self.time_played / 60

    @property
    def distance_moved_km(self):
        return self.distance_moved / 1000

    @property
    def xp_ph(self):
        return self.xp / self.time_played_hours

    @property
    def kills_ph(self):
        return self.kills / self.time_played_hours

    @property
    def deaths_ph(self):
        return self.deaths / self.time_played_hours

    @property
    def targets_destroyed_ph(self):
        return self.targets_destroyed / self.time_played_hours

    @property
    def vehicles_destroyed_ph(self):
        return self.vehicles_destroyed / self.time_played_hours

    @property
    def soldiers_healed_ph(self):
        return self.soldiers_healed / self.time_played_hours

    @property
    def team_kills_ph(self):
        return self.team_kills / self.time_played_hours

    @property
    def distance_moved_km_ph(self):
        return self.distance_moved_km / self.time_played_hours

    @property
    def shots_fired_ph(self):
        return self.shots_fired / self.time_played_hours

    @property
    def throwables_thrown_ph(self):
        return self.throwables_thrown / self.time_played_hours

    @property
    def xp_pk(self):
        return self.xp / self.kills

    @property
    def xp_pb(self):
        return self.xp / self.shots_fired

    @property
    def shots_fired_pk(self):
        return self.shots_fired / self.kills

    @property
    def team_kills_pk(self):
        return self.team_kills / self.kills

    @property
    def runs_around_the_equator(self):
        return self.distance_moved_km / earth_equat_circumference
