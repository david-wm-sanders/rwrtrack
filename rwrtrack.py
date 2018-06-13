"""rwrtrack

Usage:
    rwrtrack.py [-q|-v] get [<pages>]
    rwrtrack.py [-q|-v] analyse <name> [<othername>] [-d <dates>]
    rwrtrack.py [-q|-v] average <metric> [<minxp>] [-d <dates>]
    rwrtrack.py [-q|-v] rank <metric> [<minxp>] [<upto>] [-d <dates>]
    rwrtrack.py [-q|-v] sum [-d <dates>]
    rwrtrack.py _db_migrate_csv

Options:
    -d <dates>  Date, or two dates separated by a hyphen
                [default: latest]
                Other shortcut options: day, week, month
    -q          Quiet mode, reduces logging output to errors and above
    -v          Verbose output, with full stdout logging
"""

import logging
import logging.config
import statistics
import sys
from datetime import datetime, timedelta
from pathlib import Path

from docopt import docopt

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_

from rwrtrack.db import sesh, get_account_from_db
from rwrtrack.account import Account
from rwrtrack.record import Record
from rwrtrack.analysis import print_analysis, print_individual_analysis
from rwrtrack.avg import print_avg
from rwrtrack.get_stats import get_stats
from rwrtrack.ranking import print_ranking
from rwrtrack.stats import load_stats_from_csv, write_stats_to_csv, \
                           stats_list_to_dict, stats_dict_to_list
from rwrtrack.sums import sum_stats_and_analyse


script_dir = Path(__file__).parent
log_conf_p = (script_dir / "logging.conf").resolve()
log_p = (script_dir / "rwrtrackpy.log").resolve()
logger = logging.getLogger(__name__)


csv_hist_path = Path(__file__).parent / Path("csv_historical")


# def get_latest_csv_path():
#     csv_paths = sorted(list(csv_hist_path.glob("*.csv")), reverse=True)
#     most_recent_csv_path = csv_paths[0]
#     return most_recent_csv_path
#
#
# def load_stats_from_dates(dates):
#     if dates.isnumeric():
#         date = datetime.strptime(dates, "%Y%m%d").date()
#         csv_path = csv_hist_path / Path(f"{date}.csv")
#         stats_list = load_stats_from_csv(csv_path)
#         return stats_list_to_dict(stats_list)
#     else:
#         # Handle date ranges
#         dates = dates.split("-")
#         if dates[0] > dates[1]:
#             raise ValueError("Dates must be older-newer")
#
#         d_older = datetime.strptime(dates[0], "%Y%m%d").date()
#         csv_older = csv_hist_path / Path(f"{d_older}.csv")
#         s_older = load_stats_from_csv(csv_older)
#         d_newer = datetime.strptime(dates[1], "%Y%m%d").date()
#         csv_newer = csv_hist_path / Path(f"{d_newer}.csv")
#         s_newer = load_stats_from_csv(csv_newer)
#
#         # Diff the two datasets
#         so = stats_list_to_dict(s_older)
#         sn = stats_list_to_dict(s_newer)
#         stats_change = {}
#         for username in sn:
#             try:
#                 stats_change[username] = sn[username] - so[username]
#             except KeyError:
#                 logger.warn(f"'{username}' not in '{csv_older.name}', no diff")
#
#         return stats_change


if __name__ == '__main__':
    args = docopt(__doc__)

    log_opts = {"logfilename": log_p.as_posix(), "consoleloglvl": "INFO"}
    if args["-q"]:
        log_opts["consoleloglvl"] = "ERROR"
    elif args["-v"]:
        log_opts["consoleloglvl"] = "DEBUG"
    logging.config.fileConfig(log_conf_p.as_posix(),
                              disable_existing_loggers=False,
                              defaults=log_opts)

    logger.debug(f"Logging configured from {str(log_conf_p)}")
    logger.debug(f"Logging output will be written to {str(log_p)}")
    logger.debug(f"Running rwrtrack.py with arguments: {sys.argv[1:]}")
    logger.debug(f"docopt output:\n{args}")

    # if args["-d"].isalpha():
    #     if args["-d"] == "latest":
    #         most_recent_csv_path = get_latest_csv_path()
    #         stats_list = load_stats_from_csv(most_recent_csv_path)
    #         stats_dict = stats_list_to_dict(stats_list)
    #     elif args["-d"] == "day":
    #         most_recent_csv_path = get_latest_csv_path()
    #         dn = datetime.strptime(most_recent_csv_path.stem,
    #                                "%Y-%m-%d").date()
    #         do = dn - timedelta(days=1)
    #         dns, dos = dn.strftime("%Y%m%d"), do.strftime("%Y%m%d")
    #         stats_dict = load_stats_from_dates(f"{dos}-{dns}")
    #         stats_list = stats_dict_to_list(stats_dict)
    #     elif args["-d"] == "week":
    #         most_recent_csv_path = get_latest_csv_path()
    #         dn = datetime.strptime(most_recent_csv_path.stem,
    #                                "%Y-%m-%d").date()
    #         do = dn - timedelta(weeks=1)
    #         dns, dos = dn.strftime("%Y%m%d"), do.strftime("%Y%m%d")
    #         stats_dict = load_stats_from_dates(f"{dos}-{dns}")
    #         stats_list = stats_dict_to_list(stats_dict)
    #     else:
    #         date_opt = args["-d"]
    #         raise ValueError(f"Date(s) option '{date_opt}' invalid")
    # else:
    #     stats_dict = load_stats_from_dates(args["-d"])
    #     stats_list = stats_dict_to_list(stats_dict)

    if args["get"]:
        num_pages = int(args["<pages>"]) if args["<pages>"] else 10
        stats = get_stats(num_pages)
        write_stats_to_csv(stats)

    elif args["analyse"]:
        username = args["<name>"]
        logger.info(f"Performing individual analysis for '{username}'...")
        try:
            account = get_account_from_db(username)
            account_id = account._id
        except NoResultFound as e:
            logger.error(f"'{username}' not found in database.")
            sys.exit(1)
        if not args["<othername>"]:
            if args["-d"].isalpha():
                if args["-d"] == "latest":
                    print_analysis(account.latest_record)
                elif args["-d"] == "day":
                    latest_date = account.latest_date
                    # print(latest_date)
                    d_new = datetime.strptime(str(latest_date), "%Y%m%d").date()
                    d_old = d_new - timedelta(days=1)
                    # print(d_new, d_old)
                    d_old = int(d_old.strftime("%Y%m%d"))
                    r_new = sesh.query(Record).filter_by(account_id=account_id,
                                                         date=latest_date) \
                                                        .one()
                    r_old = sesh.query(Record).filter_by(account_id=account_id,
                                                         date=d_old) \
                                                        .one()
                    print(r_new)
                    print(r_old)
                    # TODO: r_new - r_old and display!
                    # d = int(d.strftime("%Y%m%d"))
            #         most_recent_csv_path = get_latest_csv_path()
            #         dn = datetime.strptime(most_recent_csv_path.stem,
            #                                "%Y-%m-%d").date()
            #         do = dn - timedelta(days=1)
            #         dns, dos = dn.strftime("%Y%m%d"), do.strftime("%Y%m%d")
            #         stats_dict = load_stats_from_dates(f"{dos}-{dns}")
            #         stats_list = stats_dict_to_list(stats_dict)
                elif args["-d"] == "week":
                    pass
            #         most_recent_csv_path = get_latest_csv_path()
            #         dn = datetime.strptime(most_recent_csv_path.stem,
            #                                "%Y-%m-%d").date()
            #         do = dn - timedelta(weeks=1)
            #         dns, dos = dn.strftime("%Y%m%d"), do.strftime("%Y%m%d")
            #         stats_dict = load_stats_from_dates(f"{dos}-{dns}")
            #         stats_list = stats_dict_to_list(stats_dict)
                else:
                    date_opt = args["-d"]
                    raise ValueError(f"Date(s) option '{date_opt}' invalid")
            else:
                pass
            #     stats_dict = load_stats_from_dates(args["-d"])
            #     stats_list = stats_dict_to_list(stats_dict)

            # print_individual_analysis(stats_dict, name)

            # print(account)
            # print(account.history)

        else:
            print(">do a comparative analysis")
            raise NotImplementedError()

    elif args["average"]:
        stats_pruned = [s for s in stats_list if s.time_played > 0]
        metric = args["<metric>"]
        min_xp = int(args["<minxp>"]) if args["<minxp>"] else 0
        print_avg(stats_pruned, metric, min_xp)

    elif args["rank"]:
        stats_pruned = [s for s in stats_list if s.time_played > 0]
        metric = args["<metric>"]
        min_xp = int(args["<minxp>"]) if args["<minxp>"] else 0
        upto = int(args["<upto>"]) if args["<upto>"] else 25
        print_ranking(stats_pruned, metric, min_xp, upto)

    elif args["sum"]:
        output_at_rows = [10, 100, 1000]
        sum_stats_and_analyse(stats_list, output_at_rows)

    elif args["_db_migrate_csv"]:
        logger.info("Migrating CSV to database...")

        # Configure blacklist for troublesome usernames
        username_blacklist = set()
        username_blacklist.add("RAIOORIGINAL")
        # print(username_blacklist)

        # Delete the old database
        logger.info("Obliterating the old database (temporary)...")
        db_path = Path(__file__).parent / Path("rwrtrack_history.db")
        if db_path.exists():
            db_path.unlink()

        from rwrtrack.db_base import Base
        from rwrtrack.db import engine
        Base.metadata.create_all(engine)

        # Get all CSV files and filter
        logger.info("Finding CSV files for migration...")
        csv_file_paths = sorted(list(csv_hist_path.glob("*.csv")))
        # Filter out CSV files that are not being migrated (for reasons...)
        csv_file_paths = filter(lambda x: "2017" not in x.stem, csv_file_paths)

        # TODO: Fix to load account_usernames from database
        account_usernames = set()
        for csv_file_path in csv_file_paths:
            stats = load_stats_from_csv(csv_file_path)
            # Fix dates
            d = datetime.strptime(csv_file_path.stem, "%Y-%m-%d").date()
            d = d - timedelta(days=1)
            d = int(d.strftime("%Y%m%d"))

            for s in stats:
                # If username in blacklist, skip...
                if s.username in username_blacklist:
                    continue
                if s.username not in account_usernames:
                    account_usernames.add(s.username)
                    # Create a new Account for the username
                    account = Account(username=s.username,
                                      first_date=d, latest_date=d)
                    sesh.add(account)
                    # Need to flush so that account._id is populated
                    sesh.flush()
                else:
                    account = sesh.query(Account._id) \
                                .filter_by(username=s.username).one()
                    sesh.query(Account).filter_by(_id=account._id).update(
                        {"latest_date": d})
                    # Update Account for the username
                    pass

                # Create a history entry for this stat record
                record = Record(date=d, account_id=account._id,
                                username=s.username, xp=s.xp,
                                time_played=s.time_played,
                                kills=s.kills, deaths=s.deaths,
                                score=s.score, kdr=s.kdr,
                                kill_streak=s.kill_streak,
                                targets_destroyed=s.targets_destroyed,
                                vehicles_destroyed=s.vehicles_destroyed,
                                soldiers_healed=s.soldiers_healed,
                                team_kills=s.team_kills,
                                distance_moved=s.distance_moved,
                                shots_fired=s.shots_fired,
                                throwables_thrown=s.throwables_thrown)
                sesh.add(record)

            sesh.commit()

    else:
        print(f"BAD USAGE!\n{__doc__}")
