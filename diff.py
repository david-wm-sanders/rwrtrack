import sys
from datetime import datetime, timedelta
from pathlib import Path

from stats import Stats, load_stats_from_csv, stats_to_dict
from analysis import print_analysis


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: diff.py analysis NAME DATESTART DATEEND")
        print("Usage: diff.py ranking METRIC [MINXP=0] [UPTO=50]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "analysis":
        name = sys.argv[2]
        date_start = sys.argv[3] if len(sys.argv) >= 4 else None
        date_end = sys.argv[4] if len(sys.argv) >= 5 else None
        if date_start and date_end:
            date_start = datetime.strptime(date_start, "%Y%m%d").date()
            date_end = datetime.strptime(date_end, "%Y%m%d").date()
    elif mode == "ranking":
        metric = sys.argv[2]
        min_xp = int(sys.argv[3]) if len(sys.argv) >= 4 else 0
        upto = int(sys.argv[4]) if len(sys.argv) >= 5 else 50
        date_start, date_end = None, None
    else:
        print("Usage: diff.py analysis NAME|\"NAME WITH SPACES\"")
        print("Usage: diff.py ranking METRIC [MINXP=0] [UPTO=50]")
        sys.exit(1)

    csv_hist_path = Path(__file__).parent / Path("csv_historical")
    csv_files = sorted(list(csv_hist_path.glob("*.csv")), reverse=True)
    if date_start and date_end:
        older_csv_file = csv_hist_path / Path(f"{date_start}.csv")
        newer_csv_file = csv_hist_path / Path(f"{date_end}.csv")
    else:
        newer_csv_file = csv_files[0]
        older_csv_file = csv_files[1]
    print(f"Loading {older_csv_file.name}...")
    older_stats_list = load_stats_from_csv(older_csv_file)
    print(f"Loading {newer_csv_file.name}...")
    newer__stats_list = load_stats_from_csv(newer_csv_file)
    stats_now = stats_to_dict(newer__stats_list)
    stats_then = stats_to_dict(older_stats_list)
    stats_change = {}
    for username in stats_now:
        try:
            stats_change[username] = stats_now[username] - stats_then[username]
        except KeyError:
            pass

    if mode == "analysis":
        try:
            ps = stats_change[name]
            print_analysis(ps)
        except KeyError as e:
            print(f"'{name}' not found in {newer_csv_file.name}")
            sys.exit(1)
    elif mode == "ranking":
        stats_list = []
        for s in stats_change.values():
            if s.time_played > 0:
                stats_list.append(s)
        stats_list_pruned = [s for s in stats_list if s.xp >= min_xp]
        stats_list_pruned.sort(key=lambda x: getattr(x, metric), reverse=True)
        for i, s in enumerate(stats_list_pruned, 1):
            if i > upto:
                break
            print(f"{i}: {getattr(s, metric):.2f} - {s.username} "
                  f"({s.xp}xp over {s.time_played_hours:.2f}hrs)")
