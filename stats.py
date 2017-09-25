import collections
import csv
import logging
from datetime import date
from pathlib import Path
from types import SimpleNamespace


logger = logging.getLogger(__name__)


class Stats:
    def __init__(self, username, xp, time_played, kills, deaths, kill_streak,
                 targets_destroyed, vehicles_destroyed, soldiers_healed,
                 distance_moved, shots_fired, throwables_thrown):
        self.username = username
        self.xp = xp
        self.time_played = time_played
        self.kills = kills
        self.deaths = deaths
        self.kill_streak = kill_streak
        self.targets_destroyed = targets_destroyed
        self.vehicles_destroyed = vehicles_destroyed
        self.soldiers_healed = soldiers_healed
        self.distance_moved = distance_moved
        self.shots_fired = shots_fired
        self.throwables_thrown = throwables_thrown

    @property
    def time_played_hours(self):
        return self.time_played / 60

    @property
    def distance_moved_km(self):
        return self.distance_moved / 1000

    @property
    def kdr(self):
        return self.kills / self.deaths

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
    def distance_moved_km_ph(self):
        return self.distance_moved_km / self.time_played_hours

    @property
    def shots_fired_ph(self):
        return self.shots_fired / self.time_played_hours

    @property
    def throwables_thrown_ph(self):
        return self.throwables_thrown / self.time_played_hours


def write_stats_to_csv(stats):
    date_today = date.today()
    logger.debug(f"Writing stats to {date_today}.csv")
    field_headers = ["username", "xp", "time_played",
                     "kills", "deaths", "kill_streak",
                     "targets_destroyed", "vehicles_destroyed",
                     "soldiers_healed", "distance_moved",
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
                             s.soldiers_healed, s.distance_moved,
                             s.shots_fired, s.throwables_thrown])


def load_stats_from_csv(csv_path):
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
                      distance_moved=int(r["distance_moved"]),
                      shots_fired=int(r["shots_fired"]),
                      throwables_thrown=int(r["throwables_thrown"]))
            stats.append(s)
    return stats


def stats_to_dict(stats):
    d = {}
    for s in stats:
        d[s.username] = s
    return d
