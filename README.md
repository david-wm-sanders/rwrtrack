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
### Acquiring help
`(venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py -h`
```
rwrtrack - a Running with Rifles statistics analysis tool.

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
```

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

### Analysing a player's performance on a specific date
`(venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py analyse "MR. BANG" 20170929`
```
INFO: Performing individual analysis for 'MR. BANG'...
'MR. BANG' on 20170929:
┌────────────────────┬────────────┬──────────┐
│           Statistic│       Value│  per hour│
╞════════════════════╪════════════╪══════════╡
│Time played in hours│      593.10│         1│
│                  XP│   1,806,579│  3,045.99│
│               Kills│     154,522│    260.53│
│              Deaths│       2,077│      3.50│
│   Targets destroyed│       1,540│      2.60│
│  Vehicles destroyed│       1,193│      2.01│
│     Soldiers healed│         750│      1.26│
│          Team kills│       2,016│      3.40│
│Distance moved in km│    1,438.80│      2.43│
│         Shots fired│     374,977│    632.23│
│   Throwables thrown│       1,479│      2.49│
├────────────────────┼────────────┼──────────┤
│               Score│     152,445│         -│
│                 K/D│       74.40│         -│
│        Kills per km│      107.40│         -│
│   XP per shot fired│        4.82│         -│
│         XP per kill│       11.69│         -│
│      Shots per kill│        2.43│         -│
│ Team kills per kill│     0.01305│         -│
│ Runs around equator│     0.03590│         -│
╘════════════════════╧════════════╧══════════╛
```

### Analysing the change in a player's performance between two dates
`(venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py analyse "MR. BANG" 20170929-20210813`
```
INFO: Performing individual analysis for 'MR. BANG'...
'MR. BANG' from 20170929 to 20210813:
┌────────────────────┬────────────┬──────────┐
│           Statistic│       Value│  per hour│
╞════════════════════╪════════════╪══════════╡
│Time played in hours│    1,410.18│         1│
│                  XP│   6,946,052│  4,925.64│
│               Kills│     485,710│    344.43│
│              Deaths│       1,355│      0.96│
│   Targets destroyed│       2,282│      1.62│
│  Vehicles destroyed│       2,532│      1.80│
│     Soldiers healed│       2,159│      1.53│
│          Team kills│       3,188│      2.26│
│Distance moved in km│      680.10│      0.48│
│         Shots fired│   1,613,699│  1,144.32│
│   Throwables thrown│       2,247│      1.59│
├────────────────────┼────────────┼──────────┤
│               Score│     484,355│         -│
│                 K/D│      358.46│         -│
│        Kills per km│      714.17│         -│
│   XP per shot fired│        4.30│         -│
│         XP per kill│       14.30│         -│
│      Shots per kill│        3.32│         -│
│ Team kills per kill│     0.00656│         -│
│ Runs around equator│     0.01697│         -│
╘════════════════════╧════════════╧══════════╛
```

### Ranking players by soldiers healed
* Specifying no date is like asking for the latest information
* Specifying no limit gives a default limit of 5

`(venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py rank soldiers_healed --limit=10`
```
#1       OWLCAT                  8,733
#2       RARE PEPE               8,459
#3       DOGTATO                 7,638
#4       JF 2.0                  7,527
#5       BUSTNCAPS               6,389
#6       YANKE                   5,821
#7       BIG G                   5,346
#8       HARLAND                 5,317
#9       ::PANDA::               5,246
#10      AMBULANCE               5,197
```

### Ranking players by xp per hour between two dates
* A player must be present in the records data on the first (earlier) date

`(venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py rank xp_per_hour 20210525-20210813 --limit=10`
```
Ranking by 'xp_per_hour' between 20210525 and 20210813:
#1       LINGA                   46,947.33
#2       SPIKE SPIEGEL           38,645.88
#3       PENG                    19,276.99
#4       JOLLY JELLY             19,188.00
#5       TALKINGTOTHEMOON        17,520.26
#6       FOX IN BOX              17,260.55
#7       DECEASED VETERAN        15,472.50
#8       KF EZOREDFOX            15,453.03
#9       ALZERON                 12,736.40
#10      GUOXIAOXU               12,261.56
```

### Average players with xp >= 1m | GOTA+
`(venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py average --record-filters="xp>=1000000"`
```
{'_count': 300, 'xp': 2316329.756666667, 'time_played': 60352.74333333333, 'time_played_hours': 1005.8790555555555, 'kills': 210569.06333333332, 'deaths': 7858.76, 'score': 202710.30333333332, 'kill_streak': 1242.63, 'targets_destroyed': 2959.83, 'vehicles_destroyed': 2524.8633333333332, 'soldiers_healed': 1391.5466666666666, 'team_kills': 3217.0066666666667, 'distance_moved': 2055230.6633333333, 'distance_moved_km': 2055.2306633333333, 'shots_fired': 2456487.723333333, 'throwables_thrown': 13995.22, 'runs_around_the_equator': 0.051284586188281175}
```
* `_count` is the number of records that matched the specified filters
* `--record-filters` are applied before the differencing of the records occurs and indicate conditions that the record must match at the earlier date (if a date range is specified)

### Average GOTA+ player progress between two dates
* Note that the earlier date record will be filtered for matches with record filter conditions

`(venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py average 20201231-20210813 --record-filters="xp>=1000000"`
```
{'_count': 274, 'xp': 475192.2700729927, 'time_played': 8117.069343065694, 'time_played_hours': 135.2844890510949, 'kills': 35430.32116788321, 'deaths': 774.3467153284671, 'score': 34655.97445255474, 'kill_streak': 162.4963503649635, 'targets_destroyed': 302.17518248175185, 'vehicles_destroyed': 375.3321167883212, 'soldiers_healed': 215.3905109489051, 'team_kills': 315.42335766423355, 'distance_moved': 57295.255474452555, 'distance_moved_km': 57.29525547445255, 'shots_fired': 343536.1715328467, 'throwables_thrown': 1681.463503649635, 'runs_around_the_equator': 0.0014297000915670867}
```
* Note that the \_count here is lower than^ because the number of players GOTA+|xp>=1m was 274 on 2020-12-31

### Average GOTA+ player progress between two dates where the player has played more than 60 minutes
*in the time between the two dates*

`(venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py average 20201231-20210813 --record-filters="xp>=1000000" --diff-filters="time_played>=60"`
```
{'_count': 208, 'xp': 625955.7788461539, 'time_played': 10691.009615384615, 'time_played_hours': 178.1834935897436, 'kills': 46670.8125, 'deaths': 1019.8798076923077, 'score': 45650.932692307695, 'kill_streak': 214.05769230769232, 'targets_destroyed': 398.05288461538464, 'vehicles_destroyed': 494.3701923076923, 'soldiers_healed': 283.72596153846155, 'team_kills': 415.42788461538464, 'distance_moved': 75452.88461538461, 'distance_moved_km': 75.4528846153846, 'shots_fired': 452511.36057692306, 'throwables_thrown': 2214.7451923076924, 'runs_around_the_equator': 0.0018827910819198058}
```
* Note that the \count is lower than^ because the number of players who were GOTA+ on 2020-12-31 and have played 1hr+ in the period between 2020-12-31 and 2021-08-13

### Sum top ~10k total progress
* Dateless so total progress on the latest date in db

`(venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py sum`
```
{'_count': 9998, 'xp': 1561394305, 'time_played': 72782396, 'time_played_hours': 1213039.9333333333, 'kills': 190026240, 'deaths': 20029669, 'score': 169996571, 'kill_streak': 2358400, 'targets_destroyed': 2006407, 'vehicles_destroyed': 2142945, 'soldiers_healed': 1344047, 'team_kills': 3370223, 'distance_moved': 4928652938, 'distance_moved_km': 4928652.938, 'shots_fired': 2760996801, 'throwables_thrown': 15551541, 'runs_around_the_equator': 122.98567304413122}
```
* The \_count is 9998 here for the tracked 10k because of a bug that causes a certain username to be duplicated on the official listings.
* This summation was for 2021-08-13, some interesting points:
  1. 1,561,394,305 XP is 1.5 billion and 1,213,039.9 is 1.2 million hours (or 138.47 calendar years) - you read that right! 😅
  2. 190 MILLION KILLS AND 20 MILLION DEATHS - a rough average of 190/20 or 9.5 for K/D
  3. A combined score of 169,996,571!
  4. `killstreak` is the total of the maximums that each player has achieved (and thus pretty useless?)
  5. 2,142,945 vehicles destroyed is a lot of scrap xd
  6. 2,760,996,801 - 2.76 billion shots rounds of ammunition fired... DUCK FOR COVER!
  7. Yes, runs around the equator is for Earth :D
