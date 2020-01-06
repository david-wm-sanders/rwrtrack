from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case, cast
from sqlalchemy import Float

from .constants import EARTH_EQUAT_CIRC


class DerivedStats:
    """Implements derived statistics"""
    # Score
    @hybrid_property
    def score(self):
        return self.kills - self.deaths

    # K/D ratio
    @hybrid_property
    def kdr(self):
        try:
            return self.kills / self.deaths
        except ZeroDivisionError:
            return 0

    @kdr.expression
    def kdr(cls):
        return case([(cls.deaths > 0, cast(cls.kills, Float) / cls.deaths)], else_=0)

    # Time played in hours
    @hybrid_property
    def time_played_hours(self):
        return self.time_played / 60.0

    # Distance moved in km
    @hybrid_property
    def distance_moved_km(self):
        return self.distance_moved / 1000.0

    # XP per hour
    @hybrid_property
    def xp_per_hour(self):
        try:
            return self.xp / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @xp_per_hour.expression
    def xp_per_hour(cls):
        return case([(cls.time_played > 0, cast(cls.xp, Float) / cls.time_played_hours)], else_=0)

    # Kills per hour
    @hybrid_property
    def kills_per_hour(self):
        try:
            return self.kills / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @kills_per_hour.expression
    def kills_per_hour(cls):
        return case([(cls.time_played > 0, cast(cls.kills, Float) / cls.time_played_hours)], else_=0)

    # Deaths per hour
    @hybrid_property
    def deaths_per_hour(self):
        try:
            return self.deaths / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @deaths_per_hour.expression
    def deaths_per_hour(cls):
        return case([(cls.time_played > 0, cast(cls.deaths, Float) / cls.time_played_hours)], else_=0)

    # Targets destroyed per hour
    @hybrid_property
    def targets_destroyed_per_hour(self):
        try:
            return self.targets_destroyed / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @targets_destroyed_per_hour.expression
    def targets_destroyed_per_hour(cls):
        return case([(cls.time_played > 0, cast(cls.targets_destroyed, Float) / cls.time_played_hours)], else_=0)

    # Vehicles destroyed per hour
    @hybrid_property
    def vehicles_destroyed_per_hour(self):
        try:
            return self.vehicles_destroyed / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @vehicles_destroyed_per_hour.expression
    def vehicles_destroyed_per_hour(cls):
        return case([(cls.time_played > 0, cast(cls.vehicles_destroyed, Float) / cls.time_played_hours)], else_=0)

    # Soldiers healed per hour
    @hybrid_property
    def soldiers_healed_per_hour(self):
        try:
            return self.soldiers_healed / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @soldiers_healed_per_hour.expression
    def soldiers_healed_per_hour(cls):
        return case([(cls.time_played > 0, cast(cls.soldiers_healed, Float) / cls.time_played_hours)], else_=0)

    # Team kills per hour
    @hybrid_property
    def team_kills_per_hour(self):
        try:
            return self.team_kills / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @team_kills_per_hour.expression
    def team_kills_per_hour(cls):
        return case([(cls.time_played > 0, cast(cls.team_kills, Float) / cls.time_played_hours)], else_=0)

    # Distance moved (in km) per hour
    @hybrid_property
    def distance_moved_km_per_hour(self):
        try:
            return self.distance_moved_km / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @distance_moved_km_per_hour.expression
    def distance_moved_km_per_hour(cls):
        return case([(cls.time_played > 0, cast(cls.distance_moved_km, Float) / cls.time_played_hours)], else_=0)

    # Shots fired per hour
    @hybrid_property
    def shots_fired_per_hour(self):
        try:
            return self.shots_fired / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @shots_fired_per_hour.expression
    def shots_fired_per_hour(cls):
        return case([(cls.time_played > 0, cast(cls.shots_fired, Float) / cls.time_played_hours)], else_=0)

    # Throwables thrown per hour
    @hybrid_property
    def throwables_thrown_per_hour(self):
        try:
            return self.throwables_thrown / self.time_played_hours
        except ZeroDivisionError:
            return 0

    @throwables_thrown_per_hour.expression
    def throwables_thrown_per_hour(cls):
        return case([(cls.time_played > 0, cast(cls.throwables_thrown, Float) / cls.time_played_hours)], else_=0)

    # Kills per km moved
    @hybrid_property
    def kills_per_km_moved(self):
        try:
            return self.kills / self.distance_moved_km
        except ZeroDivisionError:
            return 0

    @kills_per_km_moved.expression
    def kills_per_km_moved(cls):
        return case([(cls.distance_moved > 0, cast(cls.kills, Float) / cls.distance_moved_km)], else_=0)

    # XP per shot fired
    @hybrid_property
    def xp_per_shot_fired(self):
        try:
            return self.xp / self.shots_fired
        except ZeroDivisionError:
            return 0

    @xp_per_shot_fired.expression
    def xp_per_shot_fired(cls):
        return case([(cls.shots_fired > 0, cast(cls.xp, Float) / cls.shots_fired)], else_=0)

    # XP per kill
    @hybrid_property
    def xp_per_kill(self):
        try:
            return self.xp / self.kills
        except ZeroDivisionError:
            return 0

    @xp_per_kill.expression
    def xp_per_kill(cls):
        return case([(cls.kills > 0, cast(cls.xp, Float) / cls.kills)], else_=0)

    # Shots fired per kill
    @hybrid_property
    def shots_fired_per_kill(self):
        try:
            return self.shots_fired / self.kills
        except ZeroDivisionError:
            return 0

    @shots_fired_per_kill.expression
    def shots_fired_per_kill(cls):
        return case([(cls.kills > 0, cast(cls.shots_fired, Float) / cls.kills)], else_=0)

    # Team kills per kill
    @hybrid_property
    def team_kills_per_kill(self):
        try:
            return self.team_kills / self.kills
        except ZeroDivisionError:
            return 0

    @team_kills_per_kill.expression
    def team_kills_per_kill(cls):
        return case([(cls.kills > 0, cast(cls.team_kills, Float) / cls.kills)], else_=0)

    # Runs around the Earth equator
    @hybrid_property
    def runs_around_the_equator(self):
        return self.distance_moved_km / EARTH_EQUAT_CIRC
