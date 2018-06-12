from sqlalchemy import Column, ForeignKey, Integer, Float, String
from db_base import Base


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
