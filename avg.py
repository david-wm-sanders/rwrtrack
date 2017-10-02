import statistics
import sys
from pathlib import Path

from stats import Stats, load_stats_from_csv


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: avg.py METRIC [MINXP=0]")
        sys.exit(1)
    metric = sys.argv[1]
    min_xp = int(sys.argv[2]) if len(sys.argv) >= 3 else 0
    csv_hist_path = Path(__file__).parent / Path("csv_historical")
    csv_files = sorted(list(csv_hist_path.glob("*.csv")), reverse=True)
    most_recent_csv_file = csv_files[0]
    print(f"Loading {most_recent_csv_file.name}...")
    stats = load_stats_from_csv(most_recent_csv_file)
    stats_pruned = [s for s in stats if s.xp >= min_xp]
    metric_mean = statistics.mean(getattr(s, metric) for s in stats_pruned)
    metric_median = statistics.median(getattr(s, metric) for s in stats_pruned)
    print(f"Mean '{metric}' is {metric_mean:.2f}")
    print(f"Median '{metric}' is {metric_median:.2f}")
