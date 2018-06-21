import logging
import statistics

from sqlalchemy.orm.exc import NoResultFound

from .core import Record, get_dbinfo, get_records_on_date
from .util import process_numeric_dates, apply_filters, _dbg_write_record_ids

logger = logging.getLogger(__name__)


def perform_averaging(metric, dates, prefilters, pstfilters):
    # Fail fast if the metric specified is not one of those averageable
    if metric not in Record.metricables:
        logger.error(f"Bad metric '{metric}' can not be averaged! Exit.")
        sys.exit(1)

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
