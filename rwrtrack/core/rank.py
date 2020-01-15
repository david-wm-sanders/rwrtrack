from .db import sesh
from .record import Record
from .difference import Diff, difference
from .exceptions import NoMetricError


def rank(date, metric, usernames=None):
    q = sesh.query(Record).filter(Record.date==date)
    if usernames:
        q = q.filter(Record.username.in_(usernames))
    try:
        q = q.order_by(getattr(Record, metric).desc())
    except AttributeError as e:
        raise NoMetricError(f"Metric '{metric}' not in Record") from e
    return q


def diffrank(date_a, date_b, metric, usernames=None):
    q = difference(date_a, date_b, usernames)
    try:
        q = q.order_by(getattr(Diff, metric).desc())
    except AttributeError as e:
        raise NoMetricError(f"Metric '{metric}' not in Diff") from e
    return q
