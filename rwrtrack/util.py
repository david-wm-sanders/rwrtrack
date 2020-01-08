import logging
import sys
import operator

from .core.record import Record


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


def _write_record_names(records):
    names = [record.username for record in records]
    logger.info(f"Records: {', '.join(names)}")


def _unpack_filters(filters):
    filters_unpacked = []
    for _filter in filters.split(","):
        metric, op, value = _filter.split(":")
        filters_unpacked.append((metric, op, int(value)))
    return filters_unpacked


def _apply_filters(records, filters_unpacked):
    for metric, op, value in filters_unpacked:
        if metric not in Record.metricables:
            logger.error(f"Cannot filter by metric '{metric}'... skipping filter")
            continue
        _opmap = {">=": operator.ge, "<=": operator.le,
                  ">": operator.gt, "<": operator.lt}
        _op = _opmap.get(op, None)
        if _op:
            records = [record for record in records if _op(getattr(record, metric), value)]
        else:
            logger.error(f"Operator '{op}' not workable... skipping filter")
    return records


def apply_filters(records, filters):
    if filters:
        filters_unpacked = _unpack_filters(filters)
        records = _apply_filters(records, filters_unpacked)
    if len(records) == 0:
        logger.error("No records to average... exit.")
        sys.exit(1)
    return records
