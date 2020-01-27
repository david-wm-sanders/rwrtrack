"""rwrtrack

Usage:
    rwrtrack.py [-q|-v] get [<pages>]
    rwrtrack.py [-q|-v] analyse <name> [<dates>]
    rwrtrack.py [-q|-v] rank <metric> [<dates>] [--limit=<int>] [--record-filters=<str>] [--diff-filters=<str>]
    rwrtrack.py [-q|-v] average [<dates>] [--record-filters=<str>] [--diff-filters=<str>]
    rwrtrack.py [-q|-v] sum [<dates>] [--record-filters=<str>] [--diff-filters=<str>]
    rwrtrack.py [-q|-v] _dbinfo
    rwrtrack.py [-q|-v] _db_migrate_csv
    rwrtrack.py [-q|-v] _interact

Options:
    -q   Quiet mode, reduces logging output to errors and above
    -v   Verbose output, with full stdout logging
"""
import logging
import logging.config
from pathlib import Path

from docopt import docopt

from rwrtrack.logging import _configure_logging

from commands import _get, _analyse, _average, _rank, _sum, \
                     _dbinfo, _db_migrate_csv, _interact


logger = logging.getLogger(__name__)

script_dir = Path(__file__).parent
log_conf_path = (script_dir / "logging.conf").resolve()
log_path = (script_dir / "rwrtrackpy.log").resolve()

csv_hist_path = Path(__file__).parent / Path("csv_historical")


if __name__ == '__main__':
    args = docopt(__doc__)
    _configure_logging(log_conf_path, log_path, args)
    logger.debug(f"docopt output:\n{args}")

    if args["get"]:
        _get(args)
    elif args["analyse"]:
        _analyse(args)
    elif args["rank"]:
        _rank(args)
    elif args["average"]:
        _average(args)
    elif args["sum"]:
        _sum(args)
    elif args["_dbinfo"]:
        _dbinfo()
    elif args["_db_migrate_csv"]:
        _db_migrate_csv()
    elif args["_interact"]:
        _interact()
    else:
        print(__doc__)
