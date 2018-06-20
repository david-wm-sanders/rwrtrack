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
import operator
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
from rwrtrack.get_stats import get_stats
from rwrtrack.ranking import print_ranking
from rwrtrack.stats_csv import load_stats_from_csv, write_stats_to_csv
# from rwrtrack.sums import sum_stats_and_analyse


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
        d_older = int(dates[0])
        d_newer = int(dates[1])
        if (d_older > d_newer):
            logger.error("Dates must be older-newer!")
            sys.exit(1)
        return "range", (d_older, d_newer)


def _unpack_filters(fs):
    _fs = []
    for f in fs.split(","):
        m, o, v = f.split(":")
        _fs.append((m, o, int(v)))
    return _fs


def apply_filters(rs, filters):
    fs = _unpack_filters(filters)
    for m, o, v in fs:
        _opmap = {">": operator.ge, "<": operator.le}
        _op = _opmap.get(o, None)
        if _op:
            rs = [r for r in rs if _op(getattr(r, m), v)]
        else:
            logger.error(f"Operator '{o}' not workable... ignored")
    return rs


def _dbg_write_record_ids(rs):
    ids = [r.account_id for r in rs]
    logger.debug(f"Record ids: {ids}")


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

        logger.info(f"Performing individual analysis for '{username}'...")
        try:
            account = get_account_by_name(username)
            account_id = account._id
        except NoResultFound as e:
            logger.error(f"'{username}' not found in database.")
            sys.exit(1)
        if not othername:
            if dates.isalpha():
                if dates == "latest":
                    # print(f"'{username}' on {account.latest_date}:")
                    print(account.latest_record.as_table())
                elif dates == "first":
                    r = account.on_date(account.first_date)
                    # print(f"'{username}' on {account.first_date}:")
                    print(r.as_table())
                elif dates == "day":
                    r_newer = account.latest_record
                    r_older = account.on_date(account.latest_date, days=-1)
                    d = r_newer - r_older
                    # print(f"'{username}' from {d.dates[1]} to {d.dates[0]}:")
                    print(d.as_table())
                elif dates == "week":
                    r_newer = account.latest_record
                    r_older = account.on_date(account.latest_date, weeks=-1)
                    d = r_newer - r_older
                    # print(f"'{username}' from {d.dates[1]} to {d.dates[0]}:")
                    print(d.as_table())
                else:
                    date_opt = dates
                    raise ValueError(f"Date(s) option '{date_opt}' invalid")
            else:
                dt, d = _process_numeric_dates(dates)
                if dt == "single":
                    # TODO: Improve handling if record for date not in db
                    r = account.on_date(d)
                    # print(f"'{username}' on {r.date}:")
                    print(r.as_table())
                elif dt == "range":
                    r_newer = account.on_date(d[1])
                    r_older = account.on_date(d[0])
                    d = r_newer - r_older
                    # print(f"'{username}' from {d.dates[1]} to {d.dates[0]}:")
                    print(d.as_table())
        else:
            # print(">do a comparative analysis")
            # TODO: Implement... eventually...
            raise NotImplementedError("GO COMPARE... elsewhere until later...")

    elif args["average"]:
        # Old:
        # average <metric> [<minxp>] [-d <dates>]
        # New (provisionally):
        # average <metric> [-d <dates>] [-x <pre>] [-y <pst>]
        # TODO: Rewrite to use write to db as well
        # stats_pruned = [s for s in stats_list if s.time_played > 0]
        # min_xp = int(args["<minxp>"]) if args["<minxp>"] else 0
        # print_avg(stats_pruned, metric, min_xp)
        # TODO: Rework to allow a list of permissible metrics to be specified
        metric = args["<metric>"]
        # Fail fast if the metric specified is not one of those listed below
        if metric not in ["xp", "time_played_hours", "kills", "deaths",
                          "score", "kdr", "kill_streak", "targets_destroyed",
                          "vehicles_destroyed", "soldiers_healed",
                          "team_kills", "distance_moved_km", "shots_fired",
                          "throwables_thrown", "xp_ph", "kills_ph",
                          "deaths_ph", "targets_destroyed_ph",
                          "vehicles_destroyed_ph", "soldiers_healed_ph",
                          "team_kills_ph", "distance_moved_km_ph",
                          "shots_fired_ph", "throwables_thrown_ph",
                          "xp_pk", "xp_pb", "shots_fired_pk",
                          "team_kills_pk", "runs_around_the_equator"]:
            raise ValueError("Bad metric!")
        dates = args["-d"]
        prefilters = args["-x"]
        pstfilters = args["-y"]
        # TODO: Process filter specifiers into stuff we can operate with...
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
                raise NotImplementedError("No diffs for averages... yet...")
                # TODO: This might get complicated...
                # TODO: Get records for latest date and yesterday (relatively)
                # TODO: Apply prefilters to latest records (hereafter lrecords)
                # TODO: For each lrecord, if yrecord for id, lrecord-yrecord
                # TODO: Apply postfilters to the diffrecords
                # TODO: Average whatever is left and display...
            elif dates == "week":
                # TODO: Calculate average for metric for week
                raise NotImplementedError("No diffs for averages... yet...")
            else:
                date_opt = dates
                raise ValueError(f"Date(s) option '{date_opt}' invalid")
        else:
            dt, d = _process_numeric_dates(dates)
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
