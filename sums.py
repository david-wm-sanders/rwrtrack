from pathlib import Path

from stats import Stats, load_stats_from_csv
from analysis import print_analysis


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


if __name__ == '__main__':
    csv_hist_path = Path(__file__).parent / Path("csv_historical")
    csv_files = sorted(list(csv_hist_path.glob("*.csv")), reverse=True)
    most_recent_csv_file = csv_files[0]
    print(f"Loading {most_recent_csv_file.name}...")
    stats = load_stats_from_csv(most_recent_csv_file)
    output_at_rows = [10, 100, 1000]
    sum_stats_and_analyse(stats, output_at_rows)
