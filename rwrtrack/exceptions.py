class RwrtrackException(Exception):
    """Base class for exceptions in the rwrtrack module."""
    pass

# Exceptions for ORM-mapped database tables
class NoAccountError(RwrtrackException):
    """Raised when no 'accounts WHERE filters' in database."""
    pass

class NoRecordError(RwrtrackException):
    """Raised when no 'records WHERE filters' in database."""
    pass

# Exceptions for the filtering system in filter.py
class FilterOperatorError(RwrtrackException):
    """Raised when the operator in a filter string is unhandled."""
    pass

class FilterMetricError(RwrtrackException):
    """Raised when the metric in a filter string does not exist."""
    pass

class FilterValueError(RwrtrackException):
    """Raised when the value in a filter string can not be converted to a float."""
    pass
