"""rwrtrack

Usage:
    rwrtrack.py [-q|-v] get [<pages>]
    rwrtrack.py [-q|-v] analyse <name> [<othername>] [-d <dates>]
    rwrtrack.py [-q|-v] average <metric> [<minxp>] [-d <dates>]
    rwrtrack.py [-q|-v] rank <metric> [<minxp>] [<upto>] [-d <dates>]
    rwrtrack.py [-q|-v] sum [-d <dates>]
    rwrtrack.py [-q|-v] _db_migrate_csv

Options:
    -d <dates>  Date, or two dates separated by a hyphen
                [default: latest]
                Other shortcut options: day, week, month
    -q          Quiet mode, reduces logging output to errors and above
    -v          Verbose output, with full stdout logging
"""

import logging
import logging.config
import statistics
import sys
from datetime import datetime, timedelta
from pathlib import Path

from docopt import docopt

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_

from rwrtrack.core import DbInfo, Account, Record, sesh, get_account_from_db, \
                            update_db_from_stats
from rwrtrack.avg import print_avg
from rwrtrack.get_stats import get_stats
from rwrtrack.ranking import print_ranking
from rwrtrack.stats_csv import load_stats_from_csv, write_stats_to_csv
from rwrtrack.sums import sum_stats_and_analyse


script_dir = Path(__file__).parent
log_conf_p = (script_dir / "logging.conf").resolve()
log_p = (script_dir / "rwrtrackpy.log").resolve()
logger = logging.getLogger(__name__)


csv_hist_path = Path(__file__).parent / Path("csv_historical")


def _process_numeric_dates(date_string):
    if date_string.isnumeric():
        return "single", int(date_string)
    else:
        # Handle date ranges
        dates = date_string.split("-")
        if dates[0] > dates[1]:
            raise ValueError("Dates must be older-newer")
        d_older = int(dates[0])
        d_newer = int(dates[1])
        return "range", (d_older, d_newer)


if __name__ == '__main__':
    args = docopt(__doc__)

    log_opts = {"logfilename": log_p.as_posix(), "consoleloglvl": "INFO"}
    if args["-q"]:
        log_opts["consoleloglvl"] = "ERROR"
    elif args["-v"]:
        log_opts["consoleloglvl"] = "DEBUG"
    logging.config.fileConfig(log_conf_p.as_posix(),
                              disable_existing_loggers=False,
                              defaults=log_opts)

    logger.debug(f"Logging configured from {str(log_conf_p)}")
    logger.debug(f"Logging output will be written to {str(log_p)}")
    logger.debug(f"Running rwrtrack.py with arguments: {sys.argv[1:]}")
    logger.debug(f"docopt output:\n{args}")

    if args["get"]:
        # TODO: Rewrite to use write to db as well
        num_pages = int(args["<pages>"]) if args["<pages>"] else 10
        stats = get_stats(num_pages)
        write_stats_to_csv(stats)

    elif args["analyse"]:
        username = args["<name>"]
        logger.info(f"Performing individual analysis for '{username}'...")
        try:
            account = get_account_from_db(username)
            account_id = account._id
        except NoResultFound as e:
            logger.error(f"'{username}' not found in database.")
            sys.exit(1)
        if not args["<othername>"]:
            if args["-d"].isalpha():
                if args["-d"] == "latest":
                    print(f"'{username}' on {account.latest_date}:")
                    print(account.latest_record.as_table())
                elif args["-d"] == "first":
                    r = account.on_date(account.first_date)
                    print(f"'{username}' on {account.first_date}:")
                    print(r.as_table())
                elif args["-d"] == "day":
                    r_newer = account.latest_record
                    r_older = account.on_date(account.latest_date, days=-1)
                    d = r_newer - r_older
                    print(f"'{username}' from {d.dates[1]} to {d.dates[0]}:")
                    print(d.as_table())
                elif args["-d"] == "week":
                    r_newer = account.latest_record
                    r_older = account.on_date(account.latest_date, weeks=-1)
                    d = r_newer - r_older
                    print(f"'{username}' from {d.dates[1]} to {d.dates[0]}:")
                    print(d.as_table())
                else:
                    date_opt = args["-d"]
                    raise ValueError(f"Date(s) option '{date_opt}' invalid")
            else:
                dt, d = _process_numeric_dates(args["-d"])
                if dt == "single":
                    r = account.on_date(d)
                    print(f"'{username}' on {r.date}:")
                    print(r.as_table())
                elif dt == "range":
                    r_newer = account.on_date(d[1])
                    r_older = account.on_date(d[0])
                    d = r_newer - r_older
                    print(f"'{username}' from {d.dates[1]} to {d.dates[0]}:")
                    print(d.as_table())
        else:
            print(">do a comparative analysis")
            raise NotImplementedError()

    elif args["average"]:
        # TODO: Rewrite to use write to db as well
        # stats_pruned = [s for s in stats_list if s.time_played > 0]
        # metric = args["<metric>"]
        # min_xp = int(args["<minxp>"]) if args["<minxp>"] else 0
        # print_avg(stats_pruned, metric, min_xp)
        metric = args["<metric>"]
        print(metric)
        if args["-d"].isalpha():
            if args["-d"] == "latest":
                # TODO: Calculate average for metric on latest date
                pass
            elif args["-d"] == "first":
                pass
            elif args["-d"] == "day":
                # TODO: Calculate average for metric for day
                pass
            elif args["-d"] == "week":
                # TODO: Calculate average for metric for week
                pass
            else:
                date_opt = args["-d"]
                raise ValueError(f"Date(s) option '{date_opt}' invalid")
        else:
            dt, d = _process_numeric_dates(args["-d"])
            if dt == "single":
                # TODO: Calculate average for metric on date
                pass
            elif dt == "range":
                # TODO: Calculate average for metric across date range
                pass

    elif args["rank"]:
        # TODO: Rewrite to use write to db as well
        stats_pruned = [s for s in stats_list if s.time_played > 0]
        metric = args["<metric>"]
        min_xp = int(args["<minxp>"]) if args["<minxp>"] else 0
        upto = int(args["<upto>"]) if args["<upto>"] else 25
        print_ranking(stats_pruned, metric, min_xp, upto)

    elif args["sum"]:
        # TODO: Rewrite to use write to db as well
        output_at_rows = [10, 100, 1000]
        sum_stats_and_analyse(stats_list, output_at_rows)

    elif args["_db_migrate_csv"]:
        logger.info("Migrating CSV to database...")
        # Get all CSV files and filter
        logger.info("Finding CSV files for migration...")
        csv_file_paths = sorted(list(csv_hist_path.glob("*.csv")))
        # Filter out CSV files that are not being migrated (for reasons...)
        csv_file_paths = filter(lambda x: "2017" not in x.stem,
                                csv_file_paths)
        try:
            # Attempt to access the DbInfo
            db_info = sesh.query(DbInfo).one()
        except NoResultFound:
            # If no DbInfo, db is blank, initialise from origin CSV file
            logger.info("Blank database found - beginning full migration...")
            first_csv_path = next(csv_file_paths)
            logger.info(f"First CSV file at '{first_csv_path}'")
            # Fix dates
            d = datetime.strptime(first_csv_path.stem, "%Y-%m-%d").date()
            d = d - timedelta(days=1)
            d = int(d.strftime("%Y%m%d"))
            # Populate _dbinfo table with the initial CSV in migration
            db_info = DbInfo(first_date=d, latest_date=d)
            sesh.add(db_info)
            # Add stats from the first file in the filter generator
            stats = load_stats_from_csv(first_csv_path)
            update_db_from_stats(stats, d)
        else:
            logger.info("Existing database found - continuing migration...")
            # Step the csv_file_paths filter until we are at the first new file
            while True:
                try:
                    csv_file_path = next(csv_file_paths)
                except StopIteration:
                    logger.info("No new CSV files to migrate")
                    sys.exit(1)
                d = datetime.strptime(csv_file_path.stem, "%Y-%m-%d").date()
                d = d - timedelta(days=1)
                d = int(d.strftime("%Y%m%d"))
                if (d > db_info.latest_date):
                    # Update latest_date in _dbinfo table
                    db_info.latest_date = d
                    # Add stats from the first new file in the filter generator
                    stats = load_stats_from_csv(csv_file_path)
                    update_db_from_stats(stats, d)
                    break
        finally:
            for csv_file_path in csv_file_paths:
                stats = load_stats_from_csv(csv_file_path)
                # Fix dates
                d = datetime.strptime(csv_file_path.stem, "%Y-%m-%d").date()
                d = d - timedelta(days=1)
                d = int(d.strftime("%Y%m%d"))
                # Update latest_date in _dbinfo table
                db_info.latest_date = d
                update_db_from_stats(stats, d)

        logger.info("Committing changes to database...")
        sesh.commit()

    else:
        print(f"BAD USAGE!\n{__doc__}")
