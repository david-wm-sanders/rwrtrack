import logging
import sys
import operator

from .core import Record


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
        return "range", (d_older, d_newer)


def dbg_write_record_ids(rs):
    ids = [r.account_id for r in rs]
    logger.debug(f"Record ids: {ids}")


def _unpack_filters(fs):
    _fs = []
    for f in fs.split(","):
        m, o, v = f.split(":")
        _fs.append((m, o, int(v)))
    return _fs


def _apply_filters(rs, filters):
    fs = _unpack_filters(filters)
    for m, o, v in fs:
        if m not in Record.metricables:
            logger.error(f"Cannot filter by metric '{m}'... skipping filter")
            continue
        _opmap = {">": operator.ge, "<": operator.le}
        _op = _opmap.get(o, None)
        if _op:
            rs = [r for r in rs if _op(getattr(r, m), v)]
        else:
            logger.error(f"Operator '{o}' not workable... skipping filter")
    return rs


def apply_filters(rs, fs):
    if fs:
        rs = _apply_filters(rs, fs)
    if len(rs) == 0:
        logger.error("No records to average... exit.")
        sys.exit(1)
    return rs
