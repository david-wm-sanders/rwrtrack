import collections
import csv
import logging
from datetime import date
from pathlib import Path
from types import SimpleNamespace


logger = logging.getLogger(__name__)


# Approximate equatorial circumference of Earth
earth_equat_circumference = 40075  # km


class Stats:
    def __init__(self, username, xp, time_played, kills, deaths, kill_streak,
                 targets_destroyed, vehicles_destroyed, soldiers_healed,
                 team_kills, distance_moved, shots_fired, throwables_thrown):
        self.username = username
        self.xp = xp
        self.time_played = time_played
        self.kills = kills
        self.deaths = deaths
        self.kill_streak = kill_streak
        self.targets_destroyed = targets_destroyed
        self.vehicles_destroyed = vehicles_destroyed
        self.soldiers_healed = soldiers_healed
        self.team_kills = team_kills
        self.distance_moved = distance_moved
        self.shots_fired = shots_fired
        self.throwables_thrown = throwables_thrown

    def __repr__(self):
        return f"Stats(username={self.username}, " \
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

    def __iadd__(self, other):
        self.xp += other.xp
        self.time_played += other.time_played
        self.kills += other.kills
        self.deaths += other.deaths
        self.kill_streak += other.kill_streak
        self.targets_destroyed += other.targets_destroyed
        self.vehicles_destroyed += other.vehicles_destroyed
        self.soldiers_healed += other.soldiers_healed
        self.team_kills += other.team_kills
        self.distance_moved += other.distance_moved
        self.shots_fired += other.shots_fired
        self.throwables_thrown += other.throwables_thrown
        return self

    def __sub__(self, other):
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
        return Stats(username, xp, time_played, kills, deaths, kill_streak,
                     targets_destroyed, vehicles_destroyed, soldiers_healed,
                     team_kills, distance_moved, shots_fired,
                     throwables_thrown)

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


def write_stats_to_csv(stats):
    date_today = date.today()
    logger.info(f"Writing stats to {date_today}.csv")
    field_headers = ["username", "xp", "time_played",
                     "kills", "deaths", "kill_streak",
                     "targets_destroyed", "vehicles_destroyed",
                     "soldiers_healed", "team_kills", "distance_moved",
                     "shots_fired", "throwables_thrown"]
    csv_path = Path(__file__).parent / Path(f"csv_historical/{date_today}.csv")
    # TODO: Consider checking if a csv file for date_today already exists
    if not csv_path.parent.exists():
        csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(field_headers)
        for s in stats:
            writer.writerow([s.username, s.xp, s.time_played,
                             s.kills, s.deaths, s.kill_streak,
                             s.targets_destroyed, s.vehicles_destroyed,
                             s.soldiers_healed, s.team_kills, s.distance_moved,
                             s.shots_fired, s.throwables_thrown])


def load_stats_from_csv(csv_path):
    logger.debug(f"Loading {csv_path.name}...")
    stats = []
    with csv_path.open("r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for r in reader:
            s = Stats(username=r["username"],
                      xp=int(r["xp"]), time_played=int(r["time_played"]),
                      kills=int(r["kills"]), deaths=int(r["deaths"]),
                      kill_streak=int(r["kill_streak"]),
                      targets_destroyed=int(r["targets_destroyed"]),
                      vehicles_destroyed=int(r["vehicles_destroyed"]),
                      soldiers_healed=int(r["soldiers_healed"]),
                      # team_kills=int(r["team_kills"]),
                      team_kills=int(r.get("team_kills", 0)),
                      distance_moved=int(r["distance_moved"]),
                      shots_fired=int(r["shots_fired"]),
                      throwables_thrown=int(r["throwables_thrown"]))
            stats.append(s)
    return stats


def stats_list_to_dict(stats_list):
    d = {}
    for s in stats_list:
        d[s.username] = s
    return d


def stats_dict_to_list(stats_dict):
    l = []
    for s in stats_dict.values():
        l.append(s)
    return l
