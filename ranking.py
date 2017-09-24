import sys
from pathlib import Path

from stats import load_stats_from_csv
from analysis import calculate_metrics


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: ranking.py METRIC [MINXP=0] [UPTO=50]")
        sys.exit(1)
    sorted_by = sys.argv[1]
    min_xp = int(sys.argv[2]) if len(sys.argv) >= 3 else 0
    upto = int(sys.argv[3]) if len(sys.argv) >= 4 else 50
    csv_hist_path = Path(__file__).parent / Path("csv_historical")
    csv_files = sorted(list(csv_hist_path.glob("*.csv")), reverse=True)
    most_recent_csv_file = csv_files[0]
    print(f"Loading {most_recent_csv_file.name}...")
    stats_list = load_stats_from_csv(most_recent_csv_file)
    stats_list_pruned = [s for s in stats_list if s.xp >= min_xp]
    for s in stats_list_pruned:
        calculate_metrics(s)
    stats_list_pruned.sort(key=lambda x: getattr(x, sorted_by), reverse=True)
    for i, s in enumerate(stats_list_pruned, 1):
        if i > upto:
            break
        print(f"{i}: {getattr(s, sorted_by):.2f} - {s.username} "
              f"({s.xp}xp over {s.time_played_hours:.2f}hrs)")
