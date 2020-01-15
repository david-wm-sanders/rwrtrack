import logging
import operator

from .exceptions import NoMetricError, FilterParseError


logger = logging.getLogger(__name__)
_operator_map = {">=": operator.ge, "<=": operator.le}


def _convert_filter_str(record_type, filter_str):
    if ">=" in filter_str:
        metric, op, value = filter_str.partition(">=")
    elif "<=" in filter_str:
        metric, op, value = filter_str.partition("<=")
    else:
        return None

    _op = _operator_map[op]
    try:
        return _op(getattr(record_type, metric), float(value))
    except AttributeError as e:
        raise NoMetricError(f"Metric '{metric}' not in {record_type.__name__}") from e
    except ValueError as e:
        raise FilterParseError(f"Could not convert '{value}' to float") from e


def filter_(query, context, filters_str):
    fltr_strs = filters_str.replace(" ", "").split(",")
    for fltr_str in fltr_strs:
        try:
            fltr = _convert_filter_str(context, fltr_str)
            if fltr is not None:
                query = query.filter(fltr)
        except NoMetricError as e:
            logger.warn(f"{e} - skipping filter '{fltr_str}'")
        except FilterParseError as e:
            logger.warn(f"{e} - skipping filter '{fltr_str}'")
    return query
