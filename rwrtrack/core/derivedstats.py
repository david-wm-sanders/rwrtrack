from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case

from .constants import earth_equatorial_circumference


class DerivedStats:
    """Implements derived statistics that are not stored in columns in the Records table"""

    @hybrid_property
    def score(self):
        return self.kills - self.deaths

    @hybrid_property
    def kdr(self):
        try:
            return self.kills / self.deaths
        except ZeroDivisionError:
            return self.kills

    # Special expression case if using "kdr" directly in SQLAlchemy queries
    # This effectively mirrors the logic for the property above but as something that can be translated to SQL
    @kdr.expression
    def kdr(cls):
        return case([(cls.deaths > 0, cls.kills / cls.deaths)], else_ = cls.kills)

    @property
    def time_played_hours(self):
        return self.time_played / 60

    @property
    def distance_moved_km(self):
        return self.distance_moved / 1000

    @property
    def xp_per_hour(self):
        try:
            return self.xp / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def kills_per_hour(self):
        try:
            return self.kills / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def deaths_per_hour(self):
        try:
            return self.deaths / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def targets_destroyed_per_hour(self):
        try:
            return self.targets_destroyed / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def vehicles_destroyed_per_hour(self):
        try:
            return self.vehicles_destroyed / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def soldiers_healed_per_hour(self):
        try:
            return self.soldiers_healed / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def team_kills_per_hour(self):
        try:
            return self.team_kills / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def distance_moved_km_per_hour(self):
        try:
            return self.distance_moved_km / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def shots_fired_per_hour(self):
        try:
            return self.shots_fired / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def throwables_thrown_per_hour(self):
        try:
            return self.throwables_thrown / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @property
    def kills_per_km_moved(self):
        try:
            return self.kills / self.distance_moved_km
        except ZeroDivisionError:
            return 0

    @property
    def xp_per_shot_fired(self):
        try:
            return self.xp / self.shots_fired
        except ZeroDivisionError:
            return 0

    @property
    def xp_per_kill(self):
        try:
            return self.xp / self.kills
        except ZeroDivisionError:
            return 0

    @property
    def shots_fired_per_kill(self):
        try:
            return self.shots_fired / self.kills
        except ZeroDivisionError:
            return 0

    @property
    def team_kills_per_kill(self):
        try:
            return self.team_kills / self.kills
        except ZeroDivisionError:
            return 0

    @property
    def runs_around_the_equator(self):
        return self.distance_moved_km / earth_equatorial_circumference
