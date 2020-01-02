import logging
import statistics

from sqlalchemy.orm.exc import NoResultFound

from .core import Record, get_dbinfo, get_records_on_date
from .util import process_numeric_dates, apply_filters, _write_record_names

logger = logging.getLogger(__name__)


def calculate_averages(rs, metric):
    meanv = statistics.mean(getattr(r, metric) for r in rs)
    medianv = statistics.median(getattr(r, metric) for r in rs)
    return meanv, medianv


def _print_avgs(rs, metric):
    meanv, medianv = calculate_averages(rs, metric)
    print(f"Mean '{metric}' is {meanv:.2f}")
    print(f"Median '{metric}' is {medianv:.2f}")


def _diff_records(rs_newer, rs_older):
    rs_older = {r.account_id: r for r in rs_older}
    # For each nrecord, if orecord for id, nrecord-orecord
    rs = []
    for r_newer in rs_newer:
        acctid = r_newer.account_id
        r_older = rs_older.get(acctid, None)
        if r_older:
            diffr = r_newer - r_older
            rs.append(diffr)
    return rs


def _print_avgs_date(d, metric, prefilters):
    rs = get_records_on_date(d)
    # Apply prefilters
    logger.info(f"Applying prefilters: '{prefilters}'")
    rs = apply_filters(rs, prefilters)
    # Average whatever is left and display...
    _write_record_names(rs)
    logger.info(f"Averaging {len(rs)} records for {d}...")
    _print_avgs(rs, metric)


def _print_avgs_daterange(rs_newer, rs_older, metric, prefilters, pstfilters):
    # Apply prefilters to newer records
    logger.info(f"Applying prefilters: '{prefilters}'")
    rs_newer = apply_filters(rs_newer, prefilters)
    # Difference the records
    rs = _diff_records(rs_newer, rs_older)
    # Apply postfilters to the differenced records
    logger.info(f"Applying pstfilters: '{pstfilters}'")
    rs = apply_filters(rs, pstfilters)
    # Average whatever is left and display...
    _write_record_names(rs)
    logger.info(f"Averaging {len(rs)} records...")
    _print_avgs(rs, metric)


def perform_averaging(metric, dates, prefilters, pstfilters):
    # Fail fast if the metric specified is not one of those averageable
    if metric not in Record.metricables:
        logger.error(f"Bad metric '{metric}' can not be averaged! Exit.")
        sys.exit(1)

    logger.debug(f"Prefilters specified: '{prefilters}'")
    logger.debug(f"Pstfilters specified: '{pstfilters}'")

    try:
        db_info = get_dbinfo()
    except NoResultFound:
        print("Database is blank... Exiting.")
        sys.exit(1)

    # logger.info(f"Calculating average of '{metric}' for '{dates}'...")
    if dates.isalpha():
        if dates == "latest":
            d = db_info.latest_date
            logger.info(f"Averaging '{metric}' in records for {d}...")
            _print_avgs_date(d, metric, prefilters)
        elif dates == "first":
            d = db_info.first_date
            logger.info(f"Averaging '{metric}' in records for {d}...")
            _print_avgs_date(d, metric, prefilters)
        elif dates == "day":
            # Get records for latest date and yesterday (relatively)
            d = db_info.latest_date
            logger.info(f"Averaging '{metric}' in daily records for {d}...")
            rs_newer = get_records_on_date(d)
            rs_older = get_records_on_date(d, days=-1)
            _print_avgs_daterange(rs_newer, rs_older, metric,
                                  prefilters, pstfilters)
        elif dates == "week":
            d = db_info.latest_date
            logger.info(f"Averaging '{metric}' in weekly records for {d}...")
            rs_newer = get_records_on_date(d)
            rs_older = get_records_on_date(d, weeks=-1)
            _print_avgs_daterange(rs_newer, rs_older, metric,
                                  prefilters, pstfilters)
        elif dates == "all":
            logger.info(f"Averaging '{metric}' in historical records...")
            rs_newer = get_records_on_date(db_info.latest_date)
            rs_older = get_records_on_date(db_info.first_date)
            _print_avgs_daterange(rs_newer, rs_older, metric,
                                  prefilters, pstfilters)
        else:
            date_opt = dates
            raise ValueError(f"Date(s) option '{date_opt}' invalid")
    else:
        dt, d = process_numeric_dates(dates)
        if dt == "single":
            logger.info(f"Averaging '{metric}' in records for {d}...")
            _print_avgs_date(d, metric, prefilters)
        elif dt == "range":
            logger.info(f"Averaging '{metric}' for {d[0]}-{d[1]}...")
            rs_newer = get_records_on_date(d[1])
            rs_older = get_records_on_date(d[0])
            _print_avgs_daterange(rs_newer, rs_older, metric,
                                  prefilters, pstfilters)
