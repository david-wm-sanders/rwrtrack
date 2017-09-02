import collections
import csv
from pathlib import Path

csv_path = Path("stats_offline.csv")
Stats = collections.namedtuple("Stats",
"utc time_played game_version kills deaths team_kills killstreak " \
"targets_destroyed vehicles_destroyed soldiers_healed distance_moved " \
"shots_fired throwables_thrown rank_progression deathstreak kill_combos")

def load_stats():
    stats = []
    with csv_path.open("r") as csv_file:
        reader = csv.DictReader(csv_file)
        for r in reader:
            s = Stats(r["utc"], int(r["tp"]), int(r["gv"]), int(r["k"]),
                      int(r["d"]), int(r["tk"]), int(r["ks"]), int(r["td"]),
                      int(r["vd"]), int(r["sh"]), float(r["dm"]), int(r["sf"]),
                      int(r["tt"]), float(r["rp"]), int(r["ds"]), r["kc"])
            stats.append(s)
    return stats


if __name__ == '__main__':
    stats = load_stats()
    len_stats = len(stats)
    stats = stats[-1]
    print(f"There are {len_stats} rows of stats.")
    tp_hrs = stats.time_played/3600
    kdr = stats.kills / stats.deaths
    print(f"Latest: Time played: {tp_hrs:.2f} hours, Kills: {stats.kills}, " \
          f"Deaths: {stats.deaths}, KDR: {kdr:.2f}")
