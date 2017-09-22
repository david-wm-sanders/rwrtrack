import sys
from pathlib import Path

from stats import load_stats_from_csv
from analysis import calculate_metrics


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ranking.py METRIC")
        sys.exit(1)
    sorted_by = sys.argv[1]
    csv_hist_path = Path(__file__).parent / Path("csv_historical")
    csv_files = sorted(list(csv_hist_path.glob("*.csv")), reverse=True)
    most_recent_csv_file = csv_files[0]
    print(f"Loading {most_recent_csv_file.name}...")
    stats_list = load_stats_from_csv(most_recent_csv_file)
    for s in stats_list:
        calculate_metrics(s)
    stats_list.sort(key=lambda x: getattr(x, sorted_by), reverse=True)
    for i, s in enumerate(stats_list, 1):
        if i > 50:
            break
        print(f"{i}: {getattr(s, sorted_by):.2f} - {s.username}")
