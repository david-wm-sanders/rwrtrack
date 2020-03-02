"""Handles migration of historical statistics CSV files to the database."""
import csv
import logging
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timedelta

from .db import engine, sesh, _set_db_readonly, _set_db_writable
from .dbinfo import DbInfo, get_dbinfo
from .account import Account
from .record import Record
from .logging import _mod_logging_handlers
from .exceptions import NoCsvError, DuplicateUsernameError


logger = logging.getLogger(__name__)
# Configure blacklist for troublesome usernames
# USERNAME_BLACKLIST = set()
USERNAME_BLACKLIST = {"RAIOORIGINAL"}


@contextmanager
def _writable_db_and_reduced_file_logging():
    """Yield a writable database and reduced file logging context for a set of operations."""
    try:
        _set_db_writable()
        # Set FileHandler(s) to log at INFO to avoid debug logging every new record insertion
        _mod_logging_handlers(logging.FileHandler, logging.INFO)
        yield
    finally:
        # Set FileHandler(s) back to logging at DEBUG
        _mod_logging_handlers(logging.FileHandler, logging.DEBUG)
        _set_db_readonly()


def _find_csv_files(csv_hist_dir):
    """Find CSV files in the CSV history directory."""
    # Find CSV files in csv_hist_dir
    csv_paths = sorted(csv_hist_dir.glob("*.csv"))
    if not csv_paths:
        raise NoCsvError(f"No CSV files in '{csv_hist_dir}'")
    return csv_paths


def _fix_csv_date(csv_path):
    """Manipulate (fix) the statistics date as stored in the CSV filename to make it compatible with the database."""
    # Construct a datetime from the csv_path stem (name sans extension)
    d = datetime.strptime(csv_path.stem, "%Y-%m-%d").date()
    # Subtract a day because the CSV files are named for the date of capture not the date of the data
    d = d - timedelta(days=1)
    # Return the adjusted dt mangled into the format used by the database
    return int(d.strftime("%Y%m%d"))


def _increment(i):
    """Generate a incrementing integer count, starting at and including i."""
    while True:
        yield i
        i += 1


def migrate(csv_hist_dir):
    """Migrate CSV files stored in the csv_hist_dir into the database."""
    t0 = time.time()
    logger.info("Starting database migration...")

    with _writable_db_and_reduced_file_logging():
        logger.info(f"Finding CSV files in '{csv_hist_dir}'...")
        csv_paths = _find_csv_files(csv_hist_dir)

        logger.info(f"Inspecting database at '{engine.url}'...")
        dbinfo = get_dbinfo(error=False)
        if not dbinfo:
            # Database doesn't exist
            logger.info(f"Blank database found, starting new migration...")
            # Create dbinfo using the fixed date of the first of the CSV files
            dbinfo = DbInfo(date=_fix_csv_date(csv_paths[0]))
            sesh.add(dbinfo)
            # Create an empty account_map and instantiate an _increment generator, starting at 1
            account_map, account_id_gen = {}, _increment(1)
        else:
            # Database exists
            logger.info(f"Populated database found, continuing existing migration...")
            # Filter csv_paths for path where the fixed date is greater than the latest_date in dbinfo
            latest_date = dbinfo.latest_date
            csv_paths = [p for p in csv_paths if _fix_csv_date(p) > latest_date]
            if not csv_paths:
                raise NoCsvError(f"No new CSV files in '{csv_hist_dir}' that are eligible for migration")
            # Load accounts from db and populate an account_map from them
            account_map = {}
            accounts_in_db = sesh.query(Account).all()
            for a in accounts_in_db:
                account_map[a.username] = a._id
                last_account_id = a._id
            # Instantiate an _increment generator, starting at last_account_id + 1
            account_id_gen = _increment(last_account_id + 1)

        logger.info(f"Migrating '{csv_paths[0].name}' -> '{csv_paths[-1].name}'...")

        for csv_path in csv_paths:
            t1 = time.time()
            record_date = _fix_csv_date(csv_path)
            logger.info(f"Processing '{csv_path.name}' as '{record_date}'...")

            usernames = set()
            new_accounts, updated_accounts, new_records = [], [], []
            with csv_path.open("r", encoding="utf-8") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for r in csv_reader:
                    username = r["username"]
                    # Skip row if username is in the blacklist
                    if username in USERNAME_BLACKLIST:
                        continue
                    # Raise exception if username appears more than once in the CSV file
                    if username in usernames:
                        raise DuplicateUsernameError(f"Multiple entries for '{username}' in '{csv_path.name}'")
                    else:
                        usernames.add(username)
                    # If username doesn't already have an Account create new Account, else update the existing Account
                    if username not in account_map:
                        # Get the next account_id from the generator and map username: account_id in account_map
                        account_id = next(account_id_gen)
                        account_map[username] = account_id
                        # Create the new account dict for bulk_insert_mappings of Accounts
                        new_account = {"_id": account_id, "username": username,
                                       "first_date": record_date, "latest_date": record_date}
                        new_accounts.append(new_account)
                    else:
                        # Get the existing account_id for the username from account_map
                        account_id = account_map[username]
                        # Create the updated account dict for bulk_update_mappings of Accounts
                        updated_account = {"_id": account_id, "latest_date": record_date}
                        updated_accounts.append(updated_account)

                    # Create a new_record from the row in the CSV file
                    new_record = dict(date=record_date, account_id=account_id, username=username, xp=r["xp"],
                                      time_played=r["time_played"], kills=r["kills"], deaths=r["deaths"],
                                      kill_streak=r["kill_streak"], targets_destroyed=r["targets_destroyed"],
                                      vehicles_destroyed=r["vehicles_destroyed"], soldiers_healed=r["soldiers_healed"],
                                      team_kills=r["team_kills"], distance_moved=r["distance_moved"],
                                      shots_fired=r["shots_fired"], throwables_thrown=r["throwables_thrown"])
                    new_records.append(new_record)

            na, ua, nr = len(new_accounts), len(updated_accounts), len(new_records)
            logger.info(f"Discovered {na}/{ua} new/updated accounts across {nr} records in {(time.time() - t1):.2f}s")

            t2 = time.time()
            # Update dbinfo latest_date
            dbinfo.latest_date = record_date
            # Bulk insert new accounts
            sesh.bulk_insert_mappings(Account, new_accounts)
            # Bulk update existing accounts
            sesh.bulk_update_mappings(Account, updated_accounts)
            # Bulk insert new records
            sesh.bulk_insert_mappings(Record, new_records)
            # Commit all changes to the database atomically
            sesh.commit()

            logger.info(f"Entered mappings into database in {(time.time() - t2):.2f}s")
            logger.info(f"Migrated '{csv_path.name}' in {(time.time() - t1):.2f}s")

    # Calculate and log the time the migration took
    migration_time = time.time() - t0
    logger.info(f"Migration took {migration_time:.2f} seconds")
