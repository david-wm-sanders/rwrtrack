import collections
import csv
import logging
from datetime import date
from pathlib import Path


logger = logging.getLogger(__name__)


Stats = collections.namedtuple("Stats",
                               "username xp time_played "
                               "kills deaths longest_kill_streak "
                               "targets_destroyed vehicles_destroyed "
                               "soldiers_healed distance_moved "
                               "shots_fired throwables_thrown")


def write_stats_to_csv(stats):
    date_today = date.today()
    logger.debug(f"Writing stats to {date_today}.csv")
    field_headers = ["username", "xp", "time_played",
                     "kills", "deaths", "longest_kill_streak",
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
                             s.kills, s.deaths, s.longest_kill_streak,
                             s.targets_destroyed, s.vehicles_destroyed,
                             s.soldiers_healed, s.distance_moved,
                             s.shots_fired, s.throwables_thrown])
