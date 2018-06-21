import logging

from sqlalchemy.orm.exc import NoResultFound

from rwrtrack.core import get_account_by_name
from rwrtrack.util import process_numeric_dates

logger = logging.getLogger(__name__)


def perform_analysis(username, othername, dates):
    try:
        account = get_account_by_name(username)
        account_id = account._id
    except NoResultFound as e:
        logger.error(f"'{username}' not found in database.")
        sys.exit(1)
        
    if not othername:
        logger.info(f"Performing individual analysis for '{username}'...")
        if dates.isalpha():
            if dates == "latest":
                print(f"'{account.username}' on {account.latest_date}:")
                print(account.latest_record.as_table())
            elif dates == "first":
                r = account.on_date(account.first_date)
                print(f"'{account.username}' on {account.first_date}:")
                print(r.as_table())
            elif dates == "day":
                r_newer = account.latest_record
                r_older = account.on_date(account.latest_date, days=-1)
                d = r_newer - r_older
                print(f"'{account.username}' from "
                      f"{r_older.date} to {r_newer.date}:")
                print(d.as_table())
            elif dates == "week":
                r_newer = account.latest_record
                r_older = account.on_date(account.latest_date, weeks=-1)
                d = r_newer - r_older
                print(f"'{account.username}' from "
                      f"{r_older.date} to {r_newer.date}:")
                print(d.as_table())
            elif dates == "all":
                r_newer = account.latest_record
                r_older = account.first_record
                d = r_newer - r_older
                print(f"'{account.username}' from "
                      f"{r_older.date} to {r_newer.date}:")
                print(d.as_table())
            else:
                date_opt = dates
                raise ValueError(f"Date(s) option '{date_opt}' invalid")
        else:
            dt, d = process_numeric_dates(dates)
            if dt == "single":
                # TODO: Improve handling if record for date not in db
                r = account.on_date(d)
                print(f"'{account.username}' on {r.date}:")
                print(r.as_table())
            elif dt == "range":
                r_newer = account.on_date(d[1])
                r_older = account.on_date(d[0])
                d = r_newer - r_older
                print(f"'{account.username}' from "
                      f"{r_older.date} to {r_newer.date}:")
                print(d.as_table())
    else:
        # print(">do a comparative analysis")
        # TODO: Implement... eventually...
        raise NotImplementedError("GO COMPARE... elsewhere until later...")
