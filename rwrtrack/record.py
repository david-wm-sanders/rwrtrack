from sqlalchemy import Column, ForeignKey, Integer, Float, String

from .db_base import Base
from .derivedstats import DerivedStatsMixin
from .statsdiff import StatsDiff


class Record(Base, DerivedStatsMixin):
    __tablename__ = "records"
    date = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts._id"), primary_key=True)
    username = Column(String, nullable=False)
    xp = Column(Integer, nullable=False)
    time_played = Column(Integer, nullable=False)
    kills = Column(Integer, nullable=False)
    deaths = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    kdr = Column(Float, nullable=False)
    kill_streak = Column(Integer, nullable=False)
    targets_destroyed = Column(Integer, nullable=False)
    vehicles_destroyed = Column(Integer, nullable=False)
    soldiers_healed = Column(Integer, nullable=False)
    team_kills = Column(Integer, nullable=False)
    distance_moved = Column(Integer, nullable=False)
    shots_fired = Column(Integer, nullable=False)
    throwables_thrown = Column(Integer, nullable=False)

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
        dates = [self.date, other.date]
        account_ids = [self.account_id, other.account_id]
        usernames = [self.username, other.username]
        xp = self.xp - other.xp
        time_played = self.time_played - other.time_played
        kills = self.kills - other.kills
        deaths = self.deaths - other.deaths
        score = self.score - other.score
        kdr = self.kdr - other.kdr
        kill_streak = self.kill_streak - other.kill_streak
        targets_destroyed = self.targets_destroyed - other.targets_destroyed
        vehicles_destroyed = self.vehicles_destroyed - other.vehicles_destroyed
        soldiers_healed = self.soldiers_healed - other.soldiers_healed
        team_kills = self.team_kills - other.team_kills
        distance_moved = self.distance_moved - other.distance_moved
        shots_fired = self.shots_fired - other.shots_fired
        throwables_thrown = self.throwables_thrown - other.throwables_thrown
        return StatsDiff(dates, account_ids, usernames, xp, time_played,
                         kills, deaths, score, kdr, kill_streak,
                         targets_destroyed, vehicles_destroyed,
                         soldiers_healed, team_kills, distance_moved,
                         shots_fired, throwables_thrown)
