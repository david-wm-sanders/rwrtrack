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
from rwrtrack.exceptions import NoAccountError, NoRecordError
from rwrtrack.tablify import render_analysis_table
from rwrtrack.migrate import migrate


logger = logging.getLogger(__name__)


def process_numeric_dates(date_string):
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
        # return "range", (d_older, d_newer)
        return "range", (d_newer, d_older)


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
    migrate(csv_hist_path)


def _interact():
    print("Entering interactive mode...")
    code.interact(local=globals(), banner="", exitmsg="")
