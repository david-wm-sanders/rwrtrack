from pathlib import Path

from stats import load_stats_from_csv
from analysis import print_analysis


def sum_stats_and_analyse(stats, output_at_rows):
    xp, tp, k, d, td, vd, sh, dm, sf, tt = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for i, s in enumerate(stats, 1):
        xp += s.xp
        tp += s.time_played
        k += s.kills
        d += s.deaths
        td += s.targets_destroyed
        vd += s.vehicles_destroyed
        sh += s.soldiers_healed
        dm += s.distance_moved
        sf += s.shots_fired
        tt += s.throwables_thrown

        if i in output_at_rows:
            print(f"Number of rows summed: {i}")
            print_analysis(xp, tp, k, d, td, vd, sh, dm, sf, tt)


if __name__ == '__main__':
    csv_hist_path = Path(__file__).parent / Path("csv_historical")
    csv_files = sorted(list(csv_hist_path.glob("*.csv")), reverse=True)
    most_recent_csv_file = csv_files[0]
    print(f"Loading {most_recent_csv_file.name}...\n\n")
    stats = load_stats_from_csv(most_recent_csv_file)
    output_at_rows = [5, 10, 25, 50, 100, 250, 500, 750, 1000]
    sum_stats_and_analyse(stats, output_at_rows)
