"""rwrtrack

Usage:
    rwrtrack.py [-v] get [<pages>]
    rwrtrack.py [-v] analyse <name> [<othername>] [-d <dates>]
    rwrtrack.py [-v] average <metric> [<minxp>] [-d <dates>]
    rwrtrack.py [-v] rank <metric> [<minxp>] [<upto>] [-d <dates>]
    rwrtrack.py [-v] sum [-d <dates>]

Options:
    -d <dates>  Date, or two dates separated by a hyphen
                [default: latest]
                Other shortcut options: day, week, month
    -v          Verbose output, with full stdout logging
"""

import logging
import logging.config
import statistics
import sys
from datetime import datetime, timedelta
from pathlib import Path

from docopt import docopt

from analysis import print_analysis, print_individual_analysis
from avg import print_avg
from get_stats import get_stats
from ranking import print_ranking
from stats import load_stats_from_csv, write_stats_to_csv, \
                    stats_list_to_dict, stats_dict_to_list
from sums import sum_stats_and_analyse


script_dir = Path(__file__).parent
log_conf_p = (script_dir / "logging.conf").resolve()
log_p = (script_dir / "rwrtrackpy.log").resolve()
logger = logging.getLogger(__name__)


csv_hist_path = Path(__file__).parent / Path("csv_historical")


def get_latest_csv_path():
    csv_paths = sorted(list(csv_hist_path.glob("*.csv")), reverse=True)
    most_recent_csv_path = csv_paths[0]
    return most_recent_csv_path


def load_stats_from_dates(dates):
    if dates.isnumeric():
        date = datetime.strptime(dates, "%Y%m%d").date()
        csv_path = csv_hist_path / Path(f"{date}.csv")
        stats_list = load_stats_from_csv(csv_path)
        return stats_list_to_dict(stats_list)
    else:
        # Handle date ranges
        dates = dates.split("-")
        if dates[0] > dates[1]:
            raise ValueError("Dates must be older-newer")

        d_older = datetime.strptime(dates[0], "%Y%m%d").date()
        csv_older = csv_hist_path / Path(f"{d_older}.csv")
        s_older = load_stats_from_csv(csv_older)
        d_newer = datetime.strptime(dates[1], "%Y%m%d").date()
        csv_newer = csv_hist_path / Path(f"{d_newer}.csv")
        s_newer = load_stats_from_csv(csv_newer)

        # Diff the two datasets
        so = stats_list_to_dict(s_older)
        sn = stats_list_to_dict(s_newer)
        stats_change = {}
        for username in sn:
            try:
                stats_change[username] = sn[username] - so[username]
            except KeyError:
                logger.warn(f"'{username}' not in '{csv_older.name}', no diff")

        return stats_change


if __name__ == '__main__':
    args = docopt(__doc__)

    log_opts = {"logfilename": log_p.as_posix(), "consoleloglvl": "DEBUG"}
    if not args["-v"]:
        log_opts["consoleloglvl"] = "INFO"
    logging.config.fileConfig(log_conf_p.as_posix(),
                              disable_existing_loggers=False,
                              defaults=log_opts)

    logger.debug(f"Logging configured from {str(log_conf_p)}")
    logger.debug(f"Logging output will be written to {str(log_p)}")
    logger.debug(f"Running rwrtrack.py with arguments: {sys.argv[1:]}")
    logger.debug(f"docopt output:\n{args}")

    if args["-d"].isalpha():
        if args["-d"] == "latest":
            most_recent_csv_path = get_latest_csv_path()
            stats_list = load_stats_from_csv(most_recent_csv_path)
            stats_dict = stats_list_to_dict(stats_list)
        elif args["-d"] == "day":
            most_recent_csv_path = get_latest_csv_path()
            dn = datetime.strptime(most_recent_csv_path.stem,
                                   "%Y-%m-%d").date()
            do = dn - timedelta(days=1)
            dns, dos = dn.strftime("%Y%m%d"), do.strftime("%Y%m%d")
            stats_dict = load_stats_from_dates(f"{dos}-{dns}")
            stats_list = stats_dict_to_list(stats_dict)
        elif args["-d"] == "week":
            most_recent_csv_path = get_latest_csv_path()
            dn = datetime.strptime(most_recent_csv_path.stem,
                                   "%Y-%m-%d").date()
            do = dn - timedelta(weeks=1)
            dns, dos = dn.strftime("%Y%m%d"), do.strftime("%Y%m%d")
            stats_dict = load_stats_from_dates(f"{dos}-{dns}")
            stats_list = stats_dict_to_list(stats_dict)
        else:
            date_opt = args["-d"]
            raise ValueError(f"Date(s) option '{date_opt}' invalid")
    else:
        stats_dict = load_stats_from_dates(args["-d"])
        stats_list = stats_dict_to_list(stats_dict)

    if args["get"]:
        num_pages = int(args["<pages>"]) if args["<pages>"] else 10
        stats = get_stats(num_pages)
        write_stats_to_csv(stats)

    elif args["analyse"]:
        name = args["<name>"]
        if not args["<othername>"]:
            logger.info("Performing individual analysis...")
            print_individual_analysis(stats_dict, name)
        else:
            print(">do a comparative analysis")
            raise NotImplementedError()

    elif args["average"]:
        stats_pruned = [s for s in stats_list if s.time_played > 0]
        metric = args["<metric>"]
        min_xp = int(args["<minxp>"]) if args["<minxp>"] else 0
        print_avg(stats_pruned, metric, min_xp)

    elif args["rank"]:
        stats_pruned = [s for s in stats_list if s.time_played > 0]
        metric = args["<metric>"]
        min_xp = int(args["<minxp>"]) if args["<minxp>"] else 0
        upto = int(args["<upto>"]) if args["<upto>"] else 25
        print_ranking(stats_pruned, metric, min_xp, upto)

    elif args["sum"]:
        output_at_rows = [10, 100, 1000]
        sum_stats_and_analyse(stats_list, output_at_rows)

    else:
        print(f"BAD USAGE!\n{__doc__}")
