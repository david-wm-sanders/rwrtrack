from pathlib import Path

from .stats_csv import Stats, load_stats_from_csv
from .analysis import print_analysis


def sum_stats_and_analyse(stats, output_at_rows):
    sums = Stats(username=None, xp=0, time_played=0, kills=0, deaths=0,
                 kill_streak=0, targets_destroyed=0, vehicles_destroyed=0,
                 soldiers_healed=0, team_kills=0,
                 distance_moved=0, shots_fired=0, throwables_thrown=0)
    for i, s in enumerate(stats, 1):
        sums += s
        if i in output_at_rows:
            print(f"Number of rows summed: {i}")
            print_analysis(sums)

    if len(stats) < output_at_rows[-1]:
        print(f"Number of rows summed: {len(stats)}")
        print_analysis(sums)
