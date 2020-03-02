"""Provides exceptions for the rwrtrack module."""


class RwrtrackException(Exception):  # noqa: D204
    """Base class for exceptions in the rwrtrack module."""
    pass


# Exceptions for ORM-mapped database tables
class NoAccountError(RwrtrackException):  # noqa: D204
    """Raised when no 'accounts WHERE filters' in database."""
    pass


class NoRecordError(RwrtrackException):  # noqa: D204
    """Raised when no 'records WHERE filters' in database."""
    pass


# Exceptions for the filtering system in filter.py
class FilterOperatorError(RwrtrackException):  # noqa: D204
    """Raised when the operator in a filter string is unhandled."""
    pass


class FilterMetricError(RwrtrackException):  # noqa: D204
    """Raised when the metric in a filter string does not exist."""
    pass


class FilterValueError(RwrtrackException):  # noqa: D204
    """Raised when the value in a filter string can not be converted to a float."""
    pass


# Exceptions for the CSV->database migrator in migrate.py
class NoCsvError(RwrtrackException):  # noqa: D204
    """Raised when there are no CSV files to migrate."""
    pass


class DuplicateUsernameError(RwrtrackException):  # noqa: D204
    """Raised when a duplicate username is encountered in a CSV file."""
    pass
