import logging
import sys

from rwrtrack.core import get_account_by_name
from rwrtrack.core.exceptions import NoAccountError, NoRecordError
from rwrtrack.util import process_numeric_dates
from rwrtrack.tablify import render_table

logger = logging.getLogger(__name__)


def perform_analysis(username, dates):
    try:
        account = get_account_by_name(username)
    except NoAccountError as e:
        logger.error(e)
        sys.exit(1)

    logger.info(f"Performing individual analysis for '{username}'...")
    try:
        if not dates:
            print(f"'{account.username}' on {account.latest_date}:")
            render_table(account.latest_record)
        else:
            dt, d = process_numeric_dates(dates)
            if dt == "single":
                record = account.on_date(d)
                print(f"'{account.username}' on {record.date}:")
                render_table(record)
            elif dt == "range":
                record_newer = account.on_date(d[1])
                record_older = account.on_date(d[0])
                diff = record_newer - record_older
                print(f"'{account.username}' from {record_older.date} to {record_newer.date}:")
                render_table(diff)
    except NoRecordError as e:
        logger.error(e)
