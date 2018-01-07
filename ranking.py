import sys
from pathlib import Path

from stats import load_stats_from_csv


def print_ranking(stats_list, metric, min_xp, upto):
    stats_list_pruned = [s for s in stats_list if s.xp >= min_xp]
    stats_list_pruned.sort(key=lambda x: getattr(x, metric), reverse=True)
    for i, s in enumerate(stats_list_pruned, 1):
        if i > upto:
            break
        print(f"{i}: {getattr(s, metric):.2f} - {s.username} "
              f"({s.xp}xp over {s.time_played_hours:.2f}hrs)")
