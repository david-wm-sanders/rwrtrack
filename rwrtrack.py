"""rwrtrack

Usage:
    rwrtrack.py [-q|-v] get [<pages>]
    rwrtrack.py [-q|-v] analyse <name> [<dates>]
    rwrtrack.py [-q|-v] average <metric> [-d <dates>] [-x <pre>] [-y <pst>]
    rwrtrack.py [-q|-v] _dbinfo
    rwrtrack.py [-q|-v] _db_migrate_csv
    rwrtrack.py [-q|-v] _interact

Options:
    -q          Quiet mode, reduces logging output to errors and above
    -v          Verbose output, with full stdout logging
    -d <dates>  Date, or two dates separated by a hyphen
    -x <pre>    Prefilter specifier
    -y <pst>    Postfilter specifier
"""

import logging
import logging.config
import sys
from datetime import datetime, timedelta
from pathlib import Path

from docopt import docopt

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, distinct, text

from rwrtrack.core.get import get_stats
from rwrtrack.core.csv import load_stats_from_csv, write_stats_to_csv
from rwrtrack.core.db import sesh, _set_db_readonly, _set_db_writable
from rwrtrack.core.dbinfo import DbInfo, get_dbinfo
from rwrtrack.core.account import Account, get_account_by_name
from rwrtrack.core.record import Record, get_records_on_date
from rwrtrack.core.difference import Diff, difference
from rwrtrack.core.sum import sum_, diffsum
from rwrtrack.core.average import avg, diffavg
from rwrtrack.core.rank import rank, diffrank
from rwrtrack.core.filter import filter_
from rwrtrack.core.util import update_db_from_stats
from rwrtrack.core.exceptions import NoAccountError, NoRecordError
from rwrtrack.core.tablify import render_analysis_table
from rwrtrack.core.logging import _configure_logging

from rwrtrack.util import process_numeric_dates, _write_record_names, \
                            apply_filters
from rwrtrack.averages import perform_averaging


logger = logging.getLogger(__name__)

script_dir = Path(__file__).parent
log_conf_path = (script_dir / "logging.conf").resolve()
log_path = (script_dir / "rwrtrackpy.log").resolve()

csv_hist_path = Path(__file__).parent / Path("csv_historical")


if __name__ == '__main__':
    args = docopt(__doc__)
    _configure_logging(log_conf_path, log_path, args)
    logger.debug(f"docopt output:\n{args}")

    if args["get"]:
        # TODO: Rewrite to use write to db as well
        num_pages = int(args["<pages>"]) if args["<pages>"] else 10
        stats = get_stats(num_pages)
        write_stats_to_csv(csv_hist_path, stats)

    elif args["analyse"]:
        username = args["<name>"]
        dates = args["<dates>"]
        try:
            account = get_account_by_name(username)
        except NoAccountError as e:
            logger.error(e)
            sys.exit(1)

        logger.info(f"Performing individual analysis for '{username}'...")
        try:
            if not dates:
                print(f"'{account.username}' on {account.latest_date}:")
                render_analysis_table(account.latest_record)
            else:
                dt, d = process_numeric_dates(dates)
                if dt == "single":
                    record = account.on_date(d)
                    print(f"'{account.username}' on {record.date}:")
                    render_analysis_table(record)
                elif dt == "range":
                    record_newer = account.on_date(d[1])
                    record_older = account.on_date(d[0])
                    diff = record_newer - record_older
                    print(f"'{account.username}' from {record_older.date} to {record_newer.date}:")
                    render_analysis_table(diff)
        except NoRecordError as e:
            logger.error(e)

    elif args["average"]:
        # New (provisionally):
        # average <metric> [-d <dates>] [-x <pre>] [-y <pst>]
        metric = args["<metric>"]
        dates = args["-d"]
        prefilters = args["-x"]
        pstfilters = args["-y"]
        perform_averaging(metric, dates, prefilters, pstfilters)

    elif args["_dbinfo"]:
        try:
            db_info = get_dbinfo()
        except NoResultFound:
            logger.info("Database not populated with anything. Exit.")
            sys.exit(1)

        print(f"First date: {db_info.first_date} Latest date: {db_info.latest_date}")
        num_accounts = sesh.query(func.count(Account._id)).scalar()
        print(f"Accounts recorded: {num_accounts}")
        num_days = sesh.query(func.count(distinct(Record.date))).scalar()
        print(f"Days recorded: {num_days}")
        total_records = sesh.query(func.count(Record.date)).scalar()
        print(f"Number of records: {total_records}")

    elif args["_db_migrate_csv"]:
        logger.info("Migrating CSV to database...")
        # Put the db in writable mode
        _set_db_writable()
        # Get all CSV files and filter
        logger.info("Finding CSV files for migration...")
        csv_file_paths = sorted(list(csv_hist_path.glob("*.csv")))
        # Filter out CSV files that are not being migrated (for reasons...)
        csv_file_paths = filter(lambda x: "2017" not in x.stem and "2018" not in x.stem,
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
                logger.info(f"Processing CSV file at '{csv_file_path}'...")
                stats = load_stats_from_csv(csv_file_path)
                # Fix dates
                d = datetime.strptime(csv_file_path.stem, "%Y-%m-%d").date()
                d = d - timedelta(days=1)
                d = int(d.strftime("%Y%m%d"))
                # Update latest_date in _dbinfo table
                db_info.latest_date = d
                update_db_from_stats(stats, d)
                # logger.info("Committing changes to database...")
                sesh.commit()

        # Return the db to readonly mode
        _set_db_readonly()

    elif args["_interact"]:
        print("Entering interactive mode...")
        import code
        _dbinfo = get_dbinfo()
        _bang = get_account_by_name("MR. BANG")
        _bang_diff_q = difference(20191231, 20181231, ["MR. BANG"])
        _bang_diff = _bang_diff_q.one()._asdict()
        code.interact(local=locals(), banner="", exitmsg="")

    else:
        print(f"BAD USAGE!\n{__doc__}")
