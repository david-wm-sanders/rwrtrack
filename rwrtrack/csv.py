"""Provides functionality for writing/reading RWR statistics to/from CSV files."""
import csv
import logging
from datetime import date
from pathlib import Path


logger = logging.getLogger(__name__)


class Stats:
    """Stores associated RWR statistics."""

    def __init__(self, username, xp, time_played, kills, deaths, kill_streak,
                 targets_destroyed, vehicles_destroyed, soldiers_healed,
                 team_kills, distance_moved, shots_fired, throwables_thrown):
        """Instantiate a rwrtrack Stats object."""
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
        """Return a representation of the Stats."""
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


def write_stats_to_csv(csv_hist_dir, stats):
    """Write a list of Stats to a new CSV file in csv_hist_dir."""
    dt = date.today()
    csv_path = csv_hist_dir / Path(f"{dt}.csv")
    logger.info(f"Writing stats to {csv_path.resolve()}")
    field_headers = ["username", "xp", "time_played",
                     "kills", "deaths", "kill_streak",
                     "targets_destroyed", "vehicles_destroyed",
                     "soldiers_healed", "team_kills", "distance_moved",
                     "shots_fired", "throwables_thrown"]
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
    """Load statistics from a CSV file at csv_path and return them as a list of Stats."""
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
                      team_kills=int(r["team_kills"]),
                      distance_moved=int(r["distance_moved"]),
                      shots_fired=int(r["shots_fired"]),
                      throwables_thrown=int(r["throwables_thrown"]))
            stats.append(s)
    return stats
