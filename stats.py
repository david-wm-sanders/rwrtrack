import collections
import csv
import logging
from datetime import date
from pathlib import Path


logger = logging.getLogger(__name__)


Stats = collections.namedtuple("Stats",
                               "username xp time_played "
                               "kills deaths kill_streak "
                               "targets_destroyed vehicles_destroyed "
                               "soldiers_healed distance_moved "
                               "shots_fired throwables_thrown")


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
            s = Stats(r["username"], int(r["xp"]), int(r["time_played"]),
                      int(r["kills"]), int(r["deaths"]), int(r["kill_streak"]),
                      int(r["targets_destroyed"]),
                      int(r["vehicles_destroyed"]),
                      int(r["soldiers_healed"]), int(r["distance_moved"]),
                      int(r["shots_fired"]), int(r["throwables_thrown"]))
            stats.append(s)
    return stats


def stats_to_dict(stats):
    d = {}
    for s in stats:
        d[s.username] = s
    return d
