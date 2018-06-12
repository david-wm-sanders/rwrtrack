from sqlalchemy import Column, ForeignKey, Integer, Float, String

from .db_base import Base


# Approximate equatorial circumference of Earth
earth_equat_circumference = 40075  # km


class Record(Base):
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
               f"kill_streak={self.kill_streak}, " \
               f"targets_destroyed={self.targets_destroyed}, " \
               f"vehicles_destroyed={self.vehicles_destroyed}, " \
               f"soldiers_healed={self.soldiers_healed}, " \
               f"team_kills={self.team_kills}, " \
               f"distance_moved={self.distance_moved}, " \
               f"shots_fired={self.shots_fired}, " \
               f"throwables_thrown={self.throwables_thrown})"

    @property
    def time_played_hours(self):
        return self.time_played / 60

    @property
    def distance_moved_km(self):
        return self.distance_moved / 1000

    @property
    def kdr(self):
        try:
            return self.kills / self.deaths
        except ZeroDivisionError:
            return self.kills

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
    def score(self):
        return self.kills - self.deaths

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
