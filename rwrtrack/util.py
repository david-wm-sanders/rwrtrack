import logging
import time

from .db import sesh
from .account import Account
from .record import Record


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
        # return "range", (d_older, d_newer)
        return "range", (d_newer, d_older)
