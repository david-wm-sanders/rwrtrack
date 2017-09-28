import sys
from datetime import datetime, timedelta
from pathlib import Path

from stats import Stats, load_stats_from_csv, stats_to_dict
from analysis import print_analysis


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: diff.py analysis NAME")
        print("Usage: diff.py rank METRIC [MINXP=0] [UPTO=50]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "analysis":
        name = sys.argv[2]
    elif mode == "rank":
        metric = sys.argv[2]
        min_xp = int(sys.argv[3]) if len(sys.argv) >= 4 else 0
        upto = int(sys.argv[4]) if len(sys.argv) >= 5 else 50
    else:
        print("Usage: diff.py analysis NAME|\"NAME WITH SPACES\"")
        print("Usage: diff.py rank METRIC [MINXP=0] [UPTO=50]")
        sys.exit(1)

    csv_hist_path = Path(__file__).parent / Path("csv_historical")
    csv_files = sorted(list(csv_hist_path.glob("*.csv")), reverse=True)
    most_recent_csv_file = csv_files[0]
    d = datetime.strptime(most_recent_csv_file.stem, "%Y-%m-%d").date()
    d_week_ago = d - timedelta(weeks=1)
    week_ago_csv_file = csv_hist_path / Path(f"{d_week_ago}.csv")
    print(f"Loading {most_recent_csv_file.name}...")
    most_recent_stats_list = load_stats_from_csv(most_recent_csv_file)
    print(f"Loading {week_ago_csv_file.name}...")
    week_ago_stats_list = load_stats_from_csv(week_ago_csv_file)
    stats_now = stats_to_dict(most_recent_stats_list)
    stats_then = stats_to_dict(week_ago_stats_list)
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
            print(f"'{name}' not found in {most_recent_csv_file.name}")
            sys.exit(1)
    elif mode == "rank":
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
