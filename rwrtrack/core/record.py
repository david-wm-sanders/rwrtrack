import logging
from enum import Enum, unique

from sqlalchemy import orm
from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case

from .db_base import Base


logger = logging.getLogger(__name__)

# Approximate equatorial circumference of Earth
earth_equatorial_circumference = 40075  # km


class Record(Base):
    __tablename__ = "records"
    _date = Column("date", Integer, primary_key=True)
    _account_id = Column("account_id", Integer, ForeignKey("accounts._id"),
                         primary_key=True)
    _username = Column("username", String, nullable=False)
    _xp = Column("xp", Integer, nullable=False)
    _time_played = Column("time_played", Integer, nullable=False)
    _kills = Column("kills", Integer, nullable=False)
    _deaths = Column("deaths", Integer, nullable=False)
    _kill_streak = Column("kill_streak", Integer, nullable=False)
    _targets_destroyed = Column("targets_destroyed", Integer, nullable=False)
    _vehicles_destroyed = Column("vehicles_destroyed", Integer, nullable=False)
    _soldiers_healed = Column("soldiers_healed", Integer, nullable=False)
    _team_kills = Column("team_kills", Integer, nullable=False)
    _distance_moved = Column("distance_moved", Integer, nullable=False)
    _shots_fired = Column("shots_fired", Integer, nullable=False)
    _throwables_thrown = Column("throwables_thrown", Integer, nullable=False)

    metricables = ["xp", "time_played_hours", "kills", "deaths", "score",
                   "kdr", "kill_streak", "targets_destroyed",
                   "vehicles_destroyed", "soldiers_healed", "team_kills",
                   "distance_moved_km", "shots_fired", "throwables_thrown",
                   "xp_per_hour", "kills_per_hour", "deaths_per_hour", "targets_destroyed_per_hour",
                   "vehicles_destroyed_per_hour", "soldiers_healed_per_hour",
                   "team_kills_per_hour", "distance_moved_km_per_hour", "shots_fired_per_hour",
                   "throwables_thrown_per_hour", "kills_per_km_moved", "xp_per_kill", "xp_per_shot_fired",
                   "shots_fired_per_kill", "team_kills_per_kill", "runs_around_the_equator"]

    def __init__(self, date, account_id, username, xp, time_played,
                 kills, deaths, kill_streak,
                 targets_destroyed, vehicles_destroyed,
                 soldiers_healed, team_kills, distance_moved,
                 shots_fired, throwables_thrown, diff=False):
        self._date = date
        self._account_id = account_id
        self._username = username
        self._xp = xp
        self._time_played = time_played
        self._kills = kills
        self._deaths = deaths
        self._kill_streak = kill_streak
        self._targets_destroyed = targets_destroyed
        self._vehicles_destroyed = vehicles_destroyed
        self._soldiers_healed = soldiers_healed
        self._team_kills = team_kills
        self._distance_moved = distance_moved
        self._shots_fired = shots_fired
        self._throwables_thrown = throwables_thrown
        self._diff = diff

    @orm.reconstructor
    def init_on_load(self):
        self._diff = False

    @hybrid_property
    def date(self):
        return self._date

    @hybrid_property
    def account_id(self):
        return self._account_id

    @hybrid_property
    def username(self):
        return self._username

    @hybrid_property
    def xp(self):
        return self._xp

    @hybrid_property
    def time_played(self):
        return self._time_played

    @hybrid_property
    def kills(self):
        return self._kills

    @hybrid_property
    def deaths(self):
        return self._deaths

    @hybrid_property
    def kill_streak(self):
        return self._kill_streak

    @hybrid_property
    def targets_destroyed(self):
        return self._targets_destroyed

    @hybrid_property
    def vehicles_destroyed(self):
        return self._vehicles_destroyed

    @hybrid_property
    def soldiers_healed(self):
        return self._soldiers_healed

    @hybrid_property
    def team_kills(self):
        return self._team_kills

    @hybrid_property
    def distance_moved(self):
        return self._distance_moved

    @hybrid_property
    def shots_fired(self):
        return self._shots_fired

    @hybrid_property
    def throwables_thrown(self):
        return self._throwables_thrown

    def __repr__(self):
        return f"Record(date={self.date}, account_id={self.account_id}, " \
               f"username='{self.username}', " \
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

    # TODO: Move derivedstats back into class as hybridprops with exprs
    # Derived statistics (those that aren't stored as columns in the database)
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

    def __sub__(self, other):
        date = self.date
        account_id = self.account_id
        username = self.username
        xp = self.xp - other.xp
        time_played = self.time_played - other.time_played
        kills = self.kills - other.kills
        deaths = self.deaths - other.deaths
        kill_streak = self.kill_streak - other.kill_streak
        targets_destroyed = self.targets_destroyed - other.targets_destroyed
        vehicles_destroyed = self.vehicles_destroyed - other.vehicles_destroyed
        soldiers_healed = self.soldiers_healed - other.soldiers_healed
        team_kills = self.team_kills - other.team_kills
        distance_moved = self.distance_moved - other.distance_moved
        shots_fired = self.shots_fired - other.shots_fired
        throwables_thrown = self.throwables_thrown - other.throwables_thrown
        diff = (other.username, other.date)
        return Record(date, account_id, username, xp, time_played,
                      kills, deaths, kill_streak,
                      targets_destroyed, vehicles_destroyed,
                      soldiers_healed, team_kills, distance_moved,
                      shots_fired, throwables_thrown, diff=diff)

    def as_table(self):
        r = []
        # Make a beautiful table with box-drawing characters
        c0w = 20
        c1w = 12
        c2w = 10

        # Make the table header.
        r.append(f"┌{'':─<{c0w}}┬{'':─<{c1w}}┬{'':─<{c2w}}┐")
        # Make the table column headers
        r.append(f"│{'Statistic':>{c0w}}"
                 f"│{'Value':>{c1w}}│{'per hour':>{c2w}}│")
        r.append(f"╞{'':═<{c0w}}╪{'':═<{c1w}}╪{'':═<{c2w}}╡")
        # Make basic statistics rows
        tph = self.time_played_hours
        r.append(f"│{'Time played in hours':>{c0w}}"
                 f"│{tph:>{c1w},.2f}│{'1':>{c2w}}│")
        r.append(f"│{'XP':>{c0w}}│{self.xp:>{c1w},}│{self.xp_per_hour:>{c2w},.2f}│")
        r.append(f"│{'Kills':>{c0w}}"
                 f"│{self.kills:>{c1w},}│{self.kills_per_hour:>{c2w}.2f}│")
        r.append(f"│{'Deaths':>{c0w}}"
                 f"│{self.deaths:>{c1w},}│{self.deaths_per_hour:>{c2w}.2f}│")
        td, tdph = self.targets_destroyed, self.targets_destroyed_per_hour
        r.append(f"│{'Targets destroyed':>{c0w}}"
                 f"│{td:>{c1w},}│{tdph:>{c2w}.2f}│")
        vd, vdph = self.vehicles_destroyed, self.vehicles_destroyed_per_hour
        r.append(f"│{'Vehicles destroyed':>{c0w}}"
                 f"│{vd:>{c1w},}│{vdph:>{c2w}.2f}│")
        sh, shph = self.soldiers_healed, self.soldiers_healed_per_hour
        r.append(f"│{'Soldiers healed':>{c0w}}"
                 f"│{sh:>{c1w},}│{shph:>{c2w}.2f}│")
        tk, tkph = self.team_kills, self.team_kills_per_hour
        r.append(f"│{'Team kills':>{c0w}}│{tk:>{c1w},}│{tkph:>{c2w}.2f}│")
        dm, dph = self.distance_moved_km, self.distance_moved_km_per_hour
        r.append(f"│{'Distance moved in km':>{c0w}}"
                 f"│{dm:>{c1w},.2f}│{dph:>{c2w}.2f}│")
        sf, sfph = self.shots_fired, self.shots_fired_per_hour
        r.append(f"│{'Shots fired':>{c0w}}│{sf:>{c1w},}│{sfph:>{c2w},.2f}│")
        tt, ttph = self.throwables_thrown, self.throwables_thrown_per_hour
        r.append(f"│{'Throwables thrown':>{c0w}}"
                 f"│{tt:>{c1w},}│{ttph:>{c2w}.2f}│")
        # Make a table break
        r.append(f"├{'':─<{c0w}}┼{'':─<{c1w}}┼{'':─<{c2w}}┤")
        # Make some derived statistics
        r.append(f"│{'Score':>{c0w}}│{self.score:>{c1w},}│{'-':>{c2w}}│")
        r.append(f"│{'K/D':>{c0w}}│{self.kdr:>{c1w}.2f}│{'-':>{c2w}}│")
        r.append(f"│{'Kills per km':>{c0w}}"
                 f"│{self.kills_per_km_moved:>{c1w},.2f}│{'-':>{c2w}}│")
        r.append(f"│{'XP per shot fired':>{c0w}}"
                 f"│{self.xp_per_shot_fired:>{c1w},.2f}│{'-':>{c2w}}│")
        r.append(f"│{'XP per kill':>{c0w}}│"
                 f"{self.xp_per_kill:>{c1w},.2f}│{'-':>{c2w}}│")
        sf_per_kill = self.shots_fired_per_kill
        r.append(f"│{'Shots per kill':>{c0w}}"
                 f"│{sf_per_kill:>{c1w},.2f}│{'-':>{c2w}}│")
        tk_per_kill = self.team_kills_per_kill
        r.append(f"│{'Team kills per kill':>{c0w}}"
                 f"│{tk_per_kill:>{c1w},.5f}│{'-':>{c2w}}│")
        r.append(f"│{'Runs around equator':>{c0w}}"
                 f"│{self.runs_around_the_equator:>{c1w}.5f}│{'-':>{c2w}}│")
        # Make the table footer
        r.append(f"╘{'':═<{c0w}}╧{'':═<{c1w}}╧{'':═<{c2w}}╛")

        return "\n".join(r)
