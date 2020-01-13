from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import aliased
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.hybrid import hybrid_property

from .db import DeclarativeBase, sesh
from .derivedstats import DerivedStats
from .exceptions import NoRecordError


class Record(DeclarativeBase, DerivedStats):
    __tablename__ = "records"
    _date = Column("date", Integer, primary_key=True)
    _account_id = Column("account_id", Integer, ForeignKey("accounts._id"), primary_key=True)
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

    def __init__(self, date, account_id, username, xp, time_played, kills, deaths, kill_streak,
                 targets_destroyed, vehicles_destroyed, soldiers_healed, team_kills, distance_moved,
                 shots_fired, throwables_thrown):
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

    def __sub__(self, other):
        date = f"'diff:{other.date}-{self.date}'"
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
        r = Record(date, account_id, username, xp, time_played, kills, deaths, kill_streak,
                   targets_destroyed, vehicles_destroyed, soldiers_healed, team_kills, distance_moved,
                   shots_fired, throwables_thrown)
        return r


# Set aliases for Record to use in self-join scenarios
RA, RB = aliased(Record, name="ra"), aliased(Record, name="rb")


def get_records_on_date(date):
    try:
        return sesh.query(Record).filter_by(date=date).all()
    except NoResultFound as e:
        raise NoRecordError(f"No records on {date}") from e
