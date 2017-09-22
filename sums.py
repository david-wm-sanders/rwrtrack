from pathlib import Path

from stats import Stats, load_stats_from_csv
from analysis import calculate_metrics, print_analysis


def sum_stats_and_analyse(stats, output_at_rows):
    sums = Stats(xp=0, time_played=0, kills=0, deaths=0, kill_streak=0,
                  targets_destroyed=0, vehicles_destroyed=0, soldiers_healed=0,
                  distance_moved=0, shots_fired=0, throwables_thrown=0)
    for i, s in enumerate(stats, 1):
        sums.xp += s.xp
        sums.time_played += s.time_played
        sums.kills += s.kills
        sums.deaths += s.deaths
        sums.targets_destroyed += s.targets_destroyed
        sums.vehicles_destroyed += s.vehicles_destroyed
        sums.soldiers_healed += s.soldiers_healed
        sums.distance_moved += s.distance_moved
        sums.shots_fired += s.shots_fired
        sums.throwables_thrown += s.throwables_thrown

        if i in output_at_rows:
            print(f"Number of rows summed: {i}")
            calculate_metrics(sums)
            print_analysis(sums)


if __name__ == '__main__':
    csv_hist_path = Path(__file__).parent / Path("csv_historical")
    csv_files = sorted(list(csv_hist_path.glob("*.csv")), reverse=True)
    most_recent_csv_file = csv_files[0]
    print(f"Loading {most_recent_csv_file.name}...\n\n")
    stats = load_stats_from_csv(most_recent_csv_file)
    output_at_rows = [5, 10, 25, 50, 100, 250, 500, 750, 1000]
    sum_stats_and_analyse(stats, output_at_rows)
