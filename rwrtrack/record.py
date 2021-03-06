"""Defines the SQLAlchemy ORM model for a RWR player statistics record."""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import aliased
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.hybrid import hybrid_property

from .db import DeclarativeBase, sesh
from .derivedstats import DerivedStats
from .exceptions import NoRecordError


class Record(DeclarativeBase, DerivedStats):
    """Defines the SQLAlchemy ORM model for a RWR player statistics record."""

    __tablename__ = "records"
    date = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts._id"), primary_key=True)
    username = Column(String, nullable=False)
    xp = Column(Integer, nullable=False)
    time_played = Column(Integer, nullable=False)
    kills = Column(Integer, nullable=False)
    deaths = Column(Integer, nullable=False)
    kill_streak = Column(Integer, nullable=False)
    targets_destroyed = Column(Integer, nullable=False)
    vehicles_destroyed = Column(Integer, nullable=False)
    soldiers_healed = Column(Integer, nullable=False)
    team_kills = Column(Integer, nullable=False)
    distance_moved = Column(Integer, nullable=False)
    shots_fired = Column(Integer, nullable=False)
    throwables_thrown = Column(Integer, nullable=False)

    def __repr__(self):
        """Return a representation of the Record."""
        return f"Record(date={self.date}, account_id={self.account_id}, username='{self.username}', " \
               f"xp={self.xp}, time_played={self.time_played}, " \
               f"kills={self.kills}, deaths={self.deaths}, score={self.score}, kdr={self.kdr}, " \
               f"kill_streak={self.kill_streak}, " \
               f"targets_destroyed={self.targets_destroyed}, vehicles_destroyed={self.vehicles_destroyed}, " \
               f"soldiers_healed={self.soldiers_healed}, team_kills={self.team_kills}, " \
               f"distance_moved={self.distance_moved}, " \
               f"shots_fired={self.shots_fired}, throwables_thrown={self.throwables_thrown})"

    def __sub__(self, other):
        """Subtract some other Record from the Record."""
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
        r = Record(date=date, account_id=account_id, username=username, xp=xp, time_played=time_played,
                   kills=kills, deaths=deaths, kill_streak=kill_streak,
                   targets_destroyed=targets_destroyed, vehicles_destroyed=vehicles_destroyed,
                   soldiers_healed=soldiers_healed, team_kills=team_kills, distance_moved=distance_moved,
                   shots_fired=shots_fired, throwables_thrown=throwables_thrown)
        return r


# Set aliases for Record to use in self-join scenarios
RA, RB = aliased(Record, name="ra"), aliased(Record, name="rb")


def get_records_on_date(date):
    """Get all of the Records on the date."""
    try:
        return sesh.query(Record).filter_by(date=date).all()
    except NoResultFound as e:
        raise NoRecordError(f"No records on {date}") from e
