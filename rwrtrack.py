"""rwrtrack

Usage:
    rwrtrack.py [-q|-v] get [<pages>]
    rwrtrack.py [-q|-v] analyse <name> [<othername>] [-d <dates>]
    rwrtrack.py [-q|-v] average <metric> [-d <dates>] [-x <pre>] [-y <pst>]
    rwrtrack.py [-q|-v] rank <metric> [<n>] [-d <dates>] [-x <pre>] [-y <pst>]
    rwrtrack.py [-q|-v] sum [-d <dates>]
    rwrtrack.py [-q|-v] _db_migrate_csv
    rwrtrack.py [-q|-v] _interactive_mode

Options:
    -q          Quiet mode, reduces logging output to errors and above
    -v          Verbose output, with full stdout logging
    -d <dates>  Date, or two dates separated by a hyphen
                [default: latest]
                Other shortcut options: day, week, month
    -x <pre>    Prefilter specifier
    -y <pst>    Postfilter specifier
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

from rwrtrack.core import DbInfo, Account, Record, sesh, get_dbinfo, \
                            get_account_by_name, get_records_on_date, \
                            update_db_from_stats, \
                            _set_db_readonly, _set_db_writable
from rwrtrack.util import process_numeric_dates, _dbg_write_record_ids, \
                            apply_filters
from rwrtrack.analysis import perform_analysis
from rwrtrack.get_stats import get_stats
from rwrtrack.ranking import print_ranking
from rwrtrack.stats_csv import load_stats_from_csv, write_stats_to_csv
# from rwrtrack.sums import sum_stats_and_analyse


script_dir = Path(__file__).parent
log_conf_p = (script_dir / "logging.conf").resolve()
log_p = (script_dir / "rwrtrackpy.log").resolve()
logger = logging.getLogger(__name__)


csv_hist_path = Path(__file__).parent / Path("csv_historical")


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
        # analyse <name> [<othername>] [-d <dates>]
        username = args["<name>"]
        othername = args["<othername>"]
        dates = args["-d"]
        perform_analysis(username, othername, dates)

    elif args["average"]:
        # Old:
        # average <metric> [<minxp>] [-d <dates>]
        # New (provisionally):
        # average <metric> [-d <dates>] [-x <pre>] [-y <pst>]
        metric = args["<metric>"]
        # Fail fast if the metric specified is not one of those averageable
        if metric not in Record.metricables:
            logger.error(f"Bad metric '{metric}' can not be averaged! Exit.")
            sys.exit(1)
        dates = args["-d"]
        prefilters = args["-x"]
        pstfilters = args["-y"]
        logger.debug(f"Prefilters specified: '{prefilters}'")
        logger.debug(f"Postfilters specified: '{pstfilters}'")

        try:
            db_info = get_dbinfo()
        except NoResultFound:
            print("Database is blank... Exiting.")
            sys.exit(1)

        logger.info(f"Calculating average of '{metric}' for '{dates}'...")
        if dates.isalpha():
            if dates == "latest":
                d = db_info.latest_date
                rs = get_records_on_date(d)
                # Apply prefilters
                if prefilters:
                    logger.info(f"Applying prefilters: '{prefilters}'")
                    rs = apply_filters(rs, prefilters)
                if len(rs) == 0:
                    logger.error("No records to average... exit.")
                    sys.exit(1)
                logger.info(f"Averaging {len(rs)} records for {d}...")
                _dbg_write_record_ids(rs)
                meanv = statistics.mean(getattr(r, metric) for r in rs)
                medianv = statistics.median(getattr(r, metric) for r in rs)
                print(f"Mean '{metric}' is {meanv:.2f}")
                print(f"Median '{metric}' is {medianv:.2f}")
            elif dates == "first":
                d = db_info.first_date
                rs = get_records_on_date(d)
                # Apply prefilters
                if prefilters:
                    logger.info(f"Applying prefilters: '{prefilters}'")
                    rs = apply_filters(rs, prefilters)
                if len(rs) == 0:
                    logger.error("No records to average... exit.")
                    sys.exit(1)
                logger.info(f"Averaging {len(rs)} records for {d}...")
                _dbg_write_record_ids(rs)
                meanv = statistics.mean(getattr(r, metric) for r in rs)
                medianv = statistics.median(getattr(r, metric) for r in rs)
                print(f"Mean '{metric}' is {meanv:.2f}")
                print(f"Median '{metric}' is {medianv:.2f}")
            elif dates == "day":
                # TODO: Calculate average for metric for day
                # TODO: This might get complicated...
                # Get records for latest date and yesterday (relatively)
                d = db_info.latest_date
                rs_newer = get_records_on_date(d)
                rs_older = get_records_on_date(d, days=-1)
                rs_older = {r.account_id: r for r in rs_older}
                # Apply prefilters to newer records
                if prefilters:
                    rs_newer = apply_filters(rs_newer, prefilters)
                if len(rs_newer) == 0:
                    logger.error("No records to average... exit.")
                    sys.exit(1)
                # For each nrecord, if orecord for id, nrecord-orecord
                rs = []
                for r_newer in rs_newer:
                    acctid = r_newer.account_id
                    r_older = rs_older.get(acctid, None)
                    if r_older:
                        diffr = r_newer - r_older
                        rs.append(diffr)
                # Apply postfilters to the differenced records
                if pstfilters:
                    rs = apply_filters(rs, pstfilters)
                if len(rs) == 0:
                    logger.error("No records to average... exit.")
                    sys.exit(1)
                # Average whatever is left and display...
                logger.info(f"Averaging {len(rs)} daily records for {d}...")
                _dbg_write_record_ids(rs)
                meanv = statistics.mean(getattr(r, metric) for r in rs)
                medianv = statistics.median(getattr(r, metric) for r in rs)
                print(f"Mean '{metric}' is {meanv:.2f}")
                print(f"Median '{metric}' is {medianv:.2f}")
            elif dates == "week":
                # TODO: Calculate average for metric for week
                raise NotImplementedError("No diffs for averages... yet...")
            elif dates == "all":
                pass
            else:
                date_opt = dates
                raise ValueError(f"Date(s) option '{date_opt}' invalid")
        else:
            dt, d = process_numeric_dates(dates)
            if dt == "single":
                # TODO: Improve handling if record for date not in db
                rs = get_records_on_date(d)
                # Apply prefilters
                if prefilters:
                    logger.info(f"Applying prefilters: '{prefilters}'")
                    rs = apply_filters(rs, prefilters)
                if len(rs) == 0:
                    logger.error("No records to average... exit.")
                    sys.exit(1)
                logger.info(f"Averaging {len(rs)} records for {d}...")
                _dbg_write_record_ids(rs)
                meanv = statistics.mean(getattr(r, metric) for r in rs)
                medianv = statistics.median(getattr(r, metric) for r in rs)
                print(f"Mean '{metric}' is {meanv:.2f}")
                print(f"Median '{metric}' is {medianv:.2f}")
            elif dt == "range":
                # TODO: Calculate average for metric across date range
                raise NotImplementedError("No diffs for averages... yet...")

    elif args["rank"]:
        # Old:
        # rank <metric> [<minxp>] [<upto>] [-d <dates>]
        # New (provisionally):
        # rank <metric> [<n>] [-d <dates>] [-x <pre>] [-y <pst>]
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
        # Put the db in writable mode
        _set_db_writable()
        # Get all CSV files and filter
        logger.info("Finding CSV files for migration...")
        csv_file_paths = sorted(list(csv_hist_path.glob("*.csv")))
        # Filter out CSV files that are not being migrated (for reasons...)
        csv_file_paths = filter(lambda x: "2017" not in x.stem,
                                csv_file_paths)
        # TODO: Rework, just get the filter as list and peek instead...
        try:
            # Attempt to access the DbInfo
            db_info = get_dbinfo()
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
            db_info = DbInfo(date=d)
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
        # Return the db to readonly mode
        _set_db_readonly()

    elif args["_interactive_mode"]:
        print("Entering interactive mode...")
        d = get_dbinfo()
        a = get_account_by_name("MR. BANG")

    else:
        print(f"BAD USAGE!\n{__doc__}")
