import code
import logging
import sys
from datetime import datetime, timedelta

from sqlalchemy.util import KeyedTuple
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, distinct, text

from rwrtrack.get import get_stats
from rwrtrack.csv import load_stats_from_csv, write_stats_to_csv
from rwrtrack.db import sesh, _set_db_readonly, _set_db_writable
from rwrtrack.dbinfo import DbInfo, get_dbinfo
from rwrtrack.account import Account, get_account_by_name
from rwrtrack.record import Record, get_records_on_date
from rwrtrack.difference import Diff, difference
from rwrtrack.sum import sum_, diffsum
from rwrtrack.average import avg, diffavg
from rwrtrack.rank import rank, diffrank
from rwrtrack.filter import filter_
from rwrtrack.util import process_numeric_dates, update_db_from_stats
from rwrtrack.exceptions import NoAccountError, NoRecordError
from rwrtrack.tablify import render_analysis_table
from rwrtrack.logging import _configure_logging


logger = logging.getLogger(__name__)


def _get(args):
    # TODO: Rewrite to use write to db as well
    num_pages = int(args["<pages>"]) if args["<pages>"] else 10
    stats = get_stats(num_pages)
    write_stats_to_csv(csv_hist_path, stats)


def _analyse(args):
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
                record_newer = account.on_date(d[0])
                record_older = account.on_date(d[1])
                diff = record_newer - record_older
                print(f"'{account.username}' from {record_older.date} to {record_newer.date}:")
                render_analysis_table(diff)
    except NoRecordError as e:
        logger.error(e)
        sys.exit(1)


def _average(args):
    dates = args["<dates>"]
    rf, df = args["--record-filters"], args["--diff-filters"]

    if not dates:
        try:
            db_info = get_dbinfo()
            a = avg(db_info.latest_date, record_filters=rf)
        except NoResultFound:
            logger.info("Empty database! Exit.")
            sys.exit(1)
    else:
        dt, d = process_numeric_dates(dates)
        if dt == "single":
            a = avg(d, record_filters=rf)
        elif dt == "range":
            a = diffavg(d[0], d[1], record_filters=rf, diff_filters=df)

    # TODO: add nice table for averages
    print(a)


def _rank(args):
    metric = args["<metric>"]
    try:
        if args["--limit"]:
            limit = abs(int(args["--limit"]))
            if not limit > 0:
                raise ValueError
        else: limit = 5
    except ValueError as e:
        logger.error(f"Limit must be an integer greater than or equal to 1")
        sys.exit(1)
    dates = args["<dates>"]
    rf, df = args["--record-filters"], args["--diff-filters"]

    if not dates:
        try:
            db_info = get_dbinfo()
            ranking = rank(db_info.latest_date, metric, record_filters=rf)
        except NoResultFound:
            logger.info("Empty database! Exit.")
            sys.exit(1)
    else:
        dt, d = process_numeric_dates(dates)
        if dt == "single":
            ranking = rank(d, metric, record_filters=rf)
        elif dt == "range":
            ranking = diffrank(d[0], d[1], metric, record_filters=rf, diff_filters=df)

    ranking = ranking.limit(limit)
    # TODO: render ranking as table
    for r in ranking.all():
        if isinstance(r, Record):
            print(r)
        else: print(r._asdict())


def _sum(args):
    dates = args["<dates>"]
    rf, df = args["--record-filters"], args["--diff-filters"]

    if not dates:
        try:
            db_info = get_dbinfo()
            s = sum_(db_info.latest_date, record_filters=rf)
        except NoResultFound:
            logger.info("Empty database! Exit.")
            sys.exit(1)
    else:
        dt, d = process_numeric_dates(dates)
        if dt == "single":
            s = sum_(d, record_filters=rf)
        elif dt == "range":
            s = diffsum(d[0], d[1], record_filters=rf, diff_filters=df)

    # TODO: add nice table for sums
    print(s)


def _dbinfo():
    try:
        db_info = get_dbinfo()
    except NoResultFound:
        logger.info("Empty database! Exit.")
        sys.exit(1)

    print(f"First date: {db_info.first_date} Latest date: {db_info.latest_date}")
    num_accounts = sesh.query(func.count(Account._id)).scalar()
    print(f"Accounts recorded: {num_accounts}")
    num_days = sesh.query(func.count(distinct(Record.date))).scalar()
    print(f"Days recorded: {num_days}")
    total_records = sesh.query(func.count(Record.date)).scalar()
    print(f"Number of records: {total_records}")


def _db_migrate_csv(csv_hist_path):
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
        csv_file_path = next(csv_file_paths)
        logger.info(f"Processing CSV file at '{csv_file_path}'...")
        # Fix dates
        d = datetime.strptime(csv_file_path.stem, "%Y-%m-%d").date()
        d = d - timedelta(days=1)
        d = int(d.strftime("%Y%m%d"))
        # Populate _dbinfo table with the initial CSV in migration
        db_info = DbInfo(date=d)
        sesh.add(db_info)
        # Add stats from the first file in the filter generator
        stats = load_stats_from_csv(csv_file_path)
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
                logger.info(f"Processing CSV file at '{csv_file_path}'...")
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


def _interact():
    print("Entering interactive mode...")
    _db_info = get_dbinfo()
    _bang = get_account_by_name("MR. BANG")
    _bang_diff_q = difference(20191231, 20181231, ["MR. BANG"])
    _bang_diff = _bang_diff_q.one()._asdict()
    code.interact(local=locals(), banner="", exitmsg="")
