# rwrtrack
*some structures for managing a historic db of Running with Rifles official vanilla invasion stats*  
*with a wrapper command-line interface for interaction*

## Installation and Usage
### For Serpents
Not available on PyPI (yet... :eyes:) but the project follows a pythonic app structure.  
1. Have a recent Python 3 installation, definitely over 3.6 because f-strings are used... a lot. I don't think we have walrus(es: operator) here yet afa (as far as) i can remember.
2. Git clone this repo or download it from this GitHub page.
3. Make a virtual environment to contain this {project/app}'s dependencies and have it `activated`.
4. Install (pip :heart:) the requirements from `requirements.txt` into the virtual environment.
5. Acquire historic data:
    1. Download the CSV files from [rwrtrack-data](https://github.com/rwr-community-dev/rwrtrack-data) and put them in a directory `csv_historical/` relative to `rwrtrack.py`.
       * *due to legacy design choices :sweat_smile:, the CSV files are stored in a single directory and now GitHub will only show a limited number in the repo browser of rwrtrack-data xd.*
       * rwrtrack-data is only updated periodically!  \
         If you want to pull data from the official stats endpoints at your leisure you should look into `rwrtrack.py get <pages>` and the code in `rwrtrack.get` that underpins the command :)
    2. Migrate the CSV files from `csv_historical` into a `rwrtrack_history.db` with:  
       `rwrtrack.py _db_migrate_csv`
       * Migration was made 40x faster in [a commit](https://github.com/rwr-community-dev/rwrtrack/commit/59a9fe39ad533e2bd5968055d1002bc39c268eaf) so it should be fairly fast.
6. Verify you have some data in your `rwrtrack_history.db` (it should have been created at the start of first migration if it didn't exist already) with:  
   `rwrtrack.py _dbinfo`  
   * *In your terminal/console/powershell/hyperterm(!) you should see something like:*  \
     `First date: 20170929 Latest date: 20210629`  \
     `Accounts recorded: 16413`  \
     `Days recorded: 1315`  \
     `Number of records: 10350765`
7. View rwrtrack command-line help with `rwrtrack.py -h`

#### rwrtrack commands
* `-h` - print the docopt help
* `get <pages>` - acquire pages: int of data from the official rwr stats view_players endpoint and save to a CSV format
* `_db_migrate_csv` - migrate CSV files into the db
* `_dbinfo` - print information about the db
* `analyse <name> [<dates>]` - perform an analysis for required name (on optional dates - see parameters)
* `rank <metric> [<dates>] [--limit=<int>] [--record-filters=<str>] [--diff-filters=<str>]` - rank records by metric (on optional dates), limtiting by `--limit=<int>` and filtering the data with `--{record,diff}-filters=<str>`
* `average [<dates>] [--record-filters=<str>] [--diff-filters=<str>]`
* `sum [<dates>] [--record-filters=<str>] [--diff-filters=<str>]`
