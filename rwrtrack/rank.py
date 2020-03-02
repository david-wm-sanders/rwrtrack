"""Provides functionality for ranking Records and their differences."""
from .db import sesh
from .record import Record, RA
from .difference import Diff, difference
from .filter import filter_
from .exceptions import FilterMetricError


def rank(date, metric, usernames=None, record_filters=None):
    """Rank the Records on the date by the metric."""
    q = sesh.query(Record).filter(Record.date == date)
    if usernames:
        q = q.filter(Record.username.in_(usernames))
    if record_filters:
        q = filter_(q, Record, record_filters)
    try:
        q = q.order_by(getattr(Record, metric).desc())
    except AttributeError as e:
        raise FilterMetricError(f"Metric '{metric}' not in Record") from e
    return q


def diffrank(date_a, date_b, metric, usernames=None, record_filters=None, diff_filters=None):
    """Rank the difference between Records on the date_a and date_b by the metric."""
    q = difference(date_a, date_b, usernames)
    if record_filters:
        q = filter_(q, RA, record_filters)
    if diff_filters:
        q = filter_(q, Diff, diff_filters)
    try:
        q = q.order_by(getattr(Diff, metric).desc())
    except AttributeError as e:
        raise FilterMetricError(f"Metric '{metric}' not in Diff") from e
    return q
