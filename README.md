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
   * *In your terminal/console/powershell/hyperterm(!) you should see something like:*
     ```
     First date: 20170929 Latest date: 20210629
     Accounts recorded: 16413
     Days recorded: 1315
     Number of records: 10350765
     ```
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

#### rwrtrack parameters
TODO!

## Examples
### Getting official data from the endpoint
`(venv) PS C:\Users\david\projects\rwr\rwrtrack> rwrtrack.py get 1`
```
INFO: Retrieving 1 page(s) of stats from server...
INFO: Writing stats to C:\Users\david\projects\rwr\rwrtrack\csv_historical\2021-08-15.csv
```

### Migrating from CSV to database
`(venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py _db_migrate_csv`
```
INFO: Starting database migration...
INFO: Setting <FileHandler C:\Users\david\projects\rwr\rwrtrack\rwrtrackpy.log (DEBUG)> to INFO
INFO: Finding CSV files in 'C:\Users\david\projects\rwr\rwrtrack\csv_historical'...
INFO: Inspecting database at 'sqlite:///rwrtrack_history.db'...
INFO: Blank database found, starting new migration...
INFO: Migrating '2017-09-30.csv' -> '2021-08-14.csv'...
INFO: Processing '2017-09-30.csv' as '20170929'...
INFO: Discovered 1000/0 new/updated accounts across 1000 records in 0.01s
INFO: Entered mappings into database in 0.05s
INFO: Migrated '2017-09-30.csv' in 0.06s
...
INFO: Processing '2021-08-14.csv' as '20210813'...
INFO: Discovered 12/9986 new/updated accounts across 9998 records in 0.06s
INFO: Entered mappings into database in 0.31s
INFO: Migrated '2021-08-14.csv' in 0.37s
INFO: Setting <FileHandler C:\Users\david\projects\rwr\rwrtrack\rwrtrackpy.log (INFO)> to DEBUG
INFO: Migration took 415.01 seconds
```

### Checking database information
`(venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py _dbinfo`
```
First date: 20170929 Latest date: 20210813
Accounts recorded: 17025
Days recorded: 1361
Number of records: 10810673
```

### Analysing a player's performance
`(venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py analyse "MR. BANG"`
```
INFO: Performing individual analysis for 'MR. BANG'...
'MR. BANG' on 20210813:
┌────────────────────┬────────────┬──────────┐
│           Statistic│       Value│  per hour│
╞════════════════════╪════════════╪══════════╡
│Time played in hours│    2,003.28│         1│
│                  XP│   8,752,631│  4,369.14│
│               Kills│     640,232│    319.59│
│              Deaths│       3,432│      1.71│
│   Targets destroyed│       3,822│      1.91│
│  Vehicles destroyed│       3,725│      1.86│
│     Soldiers healed│       2,909│      1.45│
│          Team kills│       5,204│      2.60│
│Distance moved in km│    2,118.90│      1.06│
│         Shots fired│   1,988,676│    992.71│
│   Throwables thrown│       3,726│      1.86│
├────────────────────┼────────────┼──────────┤
│               Score│     636,800│         -│
│                 K/D│      186.55│         -│
│        Kills per km│      302.15│         -│
│   XP per shot fired│        4.40│         -│
│         XP per kill│       13.67│         -│
│      Shots per kill│        3.11│         -│
│ Team kills per kill│     0.00813│         -│
│ Runs around equator│     0.05287│         -│
╘════════════════════╧════════════╧══════════╛
```
