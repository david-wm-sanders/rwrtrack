import statistics
import sys
from pathlib import Path

from stats import Stats, load_stats_from_csv


def print_avg(stats_list, metric, min_xp):
    stats_pruned = [s for s in stats_list if s.xp >= min_xp]
    if len(stats_pruned) == 0:
        print(f"No data points for min_xp >= {min_xp}")
        sys.exit(1)
    print(f"Calculating average for {len(stats_pruned)} players...")
    metric_mean = statistics.mean(getattr(s, metric) for s in stats_pruned)
    metric_median = statistics.median(getattr(s, metric) for s in stats_pruned)
    print(f"Mean '{metric}' is {metric_mean:.2f}")
    print(f"Median '{metric}' is {metric_median:.2f}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: avg.py METRIC [MINXP=0]")
        sys.exit(1)
    metric = sys.argv[1]
    min_xp = int(sys.argv[2]) if len(sys.argv) >= 3 else 0
    csv_hist_path = Path(__file__).parent / Path("csv_historical")
    csv_files = sorted(list(csv_hist_path.glob("*.csv")), reverse=True)
    most_recent_csv_file = csv_files[0]
    stats_list = load_stats_from_csv(most_recent_csv_file)
    print_avg(stats_list, metric, min_xp)
