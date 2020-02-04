import logging
import operator

from .exceptions import FilterOperatorError, FilterMetricError, FilterValueError


logger = logging.getLogger(__name__)
_operator_map = {">=": operator.ge, "<=": operator.le}


def _convert_filter_str(record_type, filter_str):
    # TODO: add ">" and "<" operators
    if ">=" in filter_str:
        metric, op, value = filter_str.partition(">=")
    elif "<=" in filter_str:
        metric, op, value = filter_str.partition("<=")
    else:
        raise FilterOperatorError(f"Unhandled operator in '{filter_str}'")

    _op = _operator_map[op]
    try:
        return _op(getattr(record_type, metric), float(value))
    except AttributeError as e:
        raise FilterMetricError(f"Metric '{metric}' not in {record_type.__name__}") from e
    except ValueError as e:
        raise FilterValueError(f"Could not convert '{value}' to float") from e


def filter_(query, context, filters_str):
    fltr_strs = filters_str.replace(" ", "").split(",")
    for fltr_str in fltr_strs:
        try:
            fltr = _convert_filter_str(context, fltr_str)
            if fltr is not None:
                query = query.filter(fltr)
        except (FilterOperatorError, FilterMetricError, FilterValueError) as e:
            logger.warning(f"{e} - skipping filter '{fltr_str}'")
    return query
