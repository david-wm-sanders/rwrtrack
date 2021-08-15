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

*TODO: this output needs a prettified format xd - ideally render the metric we are ranking by in a special way*

`(venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py rank soldiers_healed`
```
Record(date=20210813, account_id=11252, username='OWLCAT', xp=1248454, time_played=65081, kills=102930, deaths=10548, score=92382, kdr=9.758248009101251, kill_streak=2022, targets_destroyed=4111, vehicles_destroyed=2845, soldiers_healed=8733, team_kills=4219, distance_moved=2119000, shots_fired=1087131, throwables_thrown=18550)
Record(date=20210813, account_id=10, username='RARE PEPE', xp=9547780, time_played=213485, kills=917241, deaths=23767, score=893474, kdr=38.59304918584592, kill_streak=3000, targets_destroyed=17191, vehicles_destroyed=13278, soldiers_healed=8459, team_kills=19827, distance_moved=2181600, shots_fired=8131753, throwables_thrown=74909)
Record(date=20210813, account_id=9, username='DOGTATO', xp=10365677, time_played=193434, kills=1073570, deaths=5347, score=1068223, kdr=200.77987656629887, kill_streak=3498, targets_destroyed=15486, vehicles_destroyed=10454, soldiers_healed=7638, team_kills=9306, distance_moved=2130900, shots_fired=13365870, throwables_thrown=33238)
Record(date=20210813, account_id=5710, username='JF 2.0', xp=7685520, time_played=133402, kills=528031, deaths=2726, score=525305, kdr=193.7017608217168, kill_streak=1283, targets_destroyed=9557, vehicles_destroyed=6238, soldiers_healed=7527, team_kills=3759, distance_moved=2124300, shots_fired=3379139, throwables_thrown=17238)
Record(date=20210813, account_id=11405, username='BUSTNCAPS', xp=3931798, time_played=135809, kills=357345, deaths=7885, score=349460, kdr=45.31959416613824, kill_streak=1004, targets_destroyed=5974, vehicles_destroyed=6274, soldiers_healed=6389, team_kills=4728, distance_moved=2145600, shots_fired=6018319, throwables_thrown=21717)
```
* Ranking a set of records for a single date returns an iterable of rwrtrack.record.Record which are then printed by rwrtrack

### Ranking players by xp per hour between two dates
* A player must be present in the records data on the first (earlier) date

*TODO: improve the output here*

`(venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py rank xp_per_hour 20210525-20210813`
```
(venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py rank xp_per_hour 20210525-20210813
{'account_id': 14880, 'username': 'LINGA', 'ra_date': 20210813, 'rb_date': 20210525, 'xp': 14034903, 'time_played': 17937, 'time_played_hours': 298.95, 'kills': 366687, 'deaths': 3839, 'score': 362848, 'kill_streak': 11387, 'targets_destroyed': 485, 'vehicles_destroyed': 2419, 'soldiers_healed': 48, 'team_kills': 1110, 'distance_moved': 736499, 'distance_moved_km': 736.499, 'shots_fired': 245860, 'throwables_thrown': 1165, 'kdr': 95.51628028132326, '_kdr': 56.96780848203438, 'xp_per_hour': 46947.32563973909, '_xp_per_hour': 37524.46535285285, 'kills_per_hour': 1226.5830406422479, '_kills_per_hour': 806.7355180180182, 'deaths_per_hour': 12.841612309750795, '_deaths_per_hour': -20.882500000000004, 'targets_destroyed_per_hour': 1.6223448737247033, '_targets_destroyed_per_hour': 0.7370045045045045, 'vehicles_destroyed_per_hour': 8.091654122763003, '_vehicles_destroyed_per_hour': 5.8077627627627635, 'soldiers_healed_per_hour': 0.16056196688409433, '_soldiers_healed_per_hour': 0.13513513513513514, 'team_kills_per_hour': 3.7129954841946815, '_team_kills_per_hour': -0.017117117117117164, 'distance_moved_km_per_hour': 2.4636193343368458, '_distance_moved_km_per_hour': -2.2970583708708716, 'shots_fired_per_hour': 822.4117745442381, '_shots_fired_per_hour': -1553.1535435435435, 'throwables_thrown_per_hour': 3.8969727379160397, '_throwables_thrown_per_hour': -4.500638138138137, 'kills_per_km_moved': 497.87847641340994, '_kills_per_km_moved': 319.53115931617515, 'xp_per_shot_fired': 57.084938582933376, '_xp_per_shot_fired': 34.89860859495933, 'xp_per_kill': 38.27488566543128, '_xp_per_kill': 28.29842750353069, 'shots_fired_per_kill': 0.6704900910040443, '_shots_fired_per_kill': -8.9154253348646, 'team_kills_per_kill': 0.0030271048605486424, '_team_kills_per_kill': -0.010469952146836528, 'runs_around_the_equator': 0.01837800842355226}

{'account_id': 5311, 'username': 'SPIKE SPIEGEL', 'ra_date': 20210813, 'rb_date': 20210525, 'xp': 7805179, 'time_played': 12118, 'time_played_hours': 201.96666666666667, 'kills': 205436, 'deaths': 1113, 'score': 204323, 'kill_streak': 2692, 'targets_destroyed': 230, 'vehicles_destroyed': 1741, 'soldiers_healed': 77, 'team_kills': 538, 'distance_moved': 2700, 'distance_moved_km': 2.7, 'shots_fired': 214826, 'throwables_thrown': 1630, 'kdr': 184.57861635220127, '_kdr': 
20.28856194412996, 'xp_per_hour': 38645.87720745998, '_xp_per_hour': 8450.546822631066, 'kills_per_hour': 1017.1777521043076, '_kills_per_hour': 175.91966880159976, 'deaths_per_hour': 5.510810364746658, '_deaths_per_hour': -1.5807168677187633, 'targets_destroyed_per_hour': 1.138801782472355, '_targets_destroyed_per_hour': -0.16252395950406506, 'vehicles_destroyed_per_hour': 8.620234362105958, '_vehicles_destroyed_per_hour': 1.5814347613355357, 'soldiers_healed_per_hour': 0.3812510315233537, '_soldiers_healed_per_hour': -0.25725159988901547, 'team_kills_per_hour': 2.6638059085657697, '_team_kills_per_hour': -0.3857901786783624, 'distance_moved_km_per_hour': 0.01336854266380591, '_distance_moved_km_per_hour': -0.7881892559976929, 'shots_fired_per_hour': 1063.6705727017659, '_shots_fired_per_hour': -244.18240734145024, 'throwables_thrown_per_hour': 8.070638719260604, '_throwables_thrown_per_hour': -2.077674127622389, 'kills_per_km_moved': 76087.4074074074, '_kills_per_km_moved': 97.45548966718563, 'xp_per_shot_fired': 36.332562166590634, '_xp_per_shot_fired': 4.826074560056447, 'xp_per_kill': 37.993238770225275, '_xp_per_kill': 13.673895258751534, 'shots_fired_per_kill': 1.0457076656476956, '_shots_fired_per_kill': -3.313571925025761, 'team_kills_per_kill': 0.0026188204598999202, '_team_kills_per_kill': -0.0065513464309770765, 'runs_around_the_equator': 6.737364578036237e-05}

{'account_id': 13484, 'username': 'PENG', 'ra_date': 20210813, 'rb_date': 20210525, 'xp': 3751624, 'time_played': 11677, 'time_played_hours': 194.61666666666667, 'kills': 116179, 'deaths': 928, 'score': 115251, 'kill_streak': 0, 'targets_destroyed': 238, 'vehicles_destroyed': 765, 'soldiers_healed': 108, 'team_kills': 504, 'distance_moved': 4400, 'distance_moved_km': 4.4, 'shots_fired': 307322, 'throwables_thrown': 1243, 'kdr': 125.19288793103448, '_kdr': 12.165815935497712, 'xp_per_hour': 19276.992378179326, '_xp_per_hour': 3513.9566443725657, 'kills_per_hour': 596.9632611115868, '_kills_per_hour': 53.7419116655978, 'deaths_per_hour': 4.768348034597928, '_deaths_per_hour': -0.48614326300803246, 'targets_destroyed_per_hour': 1.2229168450800718, '_targets_destroyed_per_hour': -0.251620400758513, 'vehicles_destroyed_per_hour': 3.930804144900231, '_vehicles_destroyed_per_hour': 0.1518808498978923, 'soldiers_healed_per_hour': 0.5549370557506209, '_soldiers_healed_per_hour': -0.006706467318802312, 'team_kills_per_hour': 2.589706260169564, '_team_kills_per_hour': -0.1512836437941596, 'distance_moved_km_per_hour': 0.022608546715766037, '_distance_moved_km_per_hour': -0.6863412818475911, 'shots_fired_per_hour': 1579.1144985869657, '_shots_fired_per_hour': -111.40081088961483, 'throwables_thrown_per_hour': 6.386914447203905, '_throwables_thrown_per_hour': -0.4026038242375387, 'kills_per_km_moved': 26404.31818181818, '_kills_per_km_moved': 54.834934750107266, 'xp_per_shot_fired': 12.20746968977164, '_xp_per_shot_fired': 1.8815557445258912, 'xp_per_kill': 32.291756685803804, '_xp_per_kill': 7.285090568320927, 'shots_fired_per_kill': 2.6452456984480843, '_shots_fired_per_kill': -1.0386169584651341, 'team_kills_per_kill': 0.004338133397601977, '_team_kills_per_kill': -0.001574642379237534, 'runs_around_the_equator': 0.00010979408941984979}

{'account_id': 2475, 'username': 'JOLLY JELLY', 'ra_date': 20210813, 'rb_date': 20210525, 'xp': 1599, 'time_played': 5, 'time_played_hours': 0.08333333333333333, 'kills': 53, 'deaths': 2, 'score': 51, 'kill_streak': 0, 'targets_destroyed': 0, 'vehicles_destroyed': 3, 'soldiers_healed': 0, 'team_kills': 0, 'distance_moved': 500, 'distance_moved_km': 0.5, 'shots_fired': 209, 'throwables_thrown': 4, 'kdr': 26.5, '_kdr': 0.01743651536083579, 'xp_per_hour': 19188.0, '_xp_per_hour': 20.891667526570927, 'kills_per_hour': 636.0, '_kills_per_hour': 0.5513517696831798, 'deaths_per_hour': 24.0, '_deaths_per_hour': -0.012073057476015947, 'targets_destroyed_per_hour': 0.0, '_targets_destroyed_per_hour': -0.0006346094314312323, 'vehicles_destroyed_per_hour': 36.0, '_vehicles_destroyed_per_hour': 0.03954700237333597, 'soldiers_healed_per_hour': 0.0, '_soldiers_healed_per_hour': -0.001516871323908875, 'team_kills_per_hour': 0.0, '_team_kills_per_hour': -0.0031266123207105423, 'distance_moved_km_per_hour': 6.0, '_distance_moved_km_per_hour': 0.00031420905995194204, 'shots_fired_per_hour': 2508.0, '_shots_fired_per_hour': -0.7296770199159255, 'throwables_thrown_per_hour': 48.0, '_throwables_thrown_per_hour': 0.010757403776693764, 'kills_per_km_moved': 106.0, '_kills_per_km_moved': 0.09488997206476668, 'xp_per_shot_fired': 7.650717703349282, '_xp_per_shot_fired': 0.00668955293419865, 'xp_per_kill': 30.169811320754718, '_xp_per_kill': 0.11949189379668379, 'shots_fired_per_kill': 3.943396226415094, '_shots_fired_per_kill': -0.08150100004616334, 'team_kills_per_kill': 0.0, '_team_kills_per_kill': -8.775239510105254e-05, 'runs_around_the_equator': 1.2476601070437476e-05}

{'account_id': 14129, 'username': 'TALKINGTOTHEMOON', 'ra_date': 20210813, 'rb_date': 20210525, 'xp': 956606, 'time_played': 3276, 'time_played_hours': 54.6, 'kills': 22933, 'deaths': 251, 'score': 22682, 'kill_streak': 976, 'targets_destroyed': 47, 'vehicles_destroyed': 177, 'soldiers_healed': 27, 'team_kills': 97, 'distance_moved': 141300, 'distance_moved_km': 141.3, 'shots_fired': 50348, 'throwables_thrown': 293, 'kdr': 91.36653386454184, '_kdr': 34.04744667097608, 'xp_per_hour': 17520.25641025641, '_xp_per_hour': 10536.724778705146, 'kills_per_hour': 420.018315018315, '_kills_per_hour': 130.15731034126222, 'deaths_per_hour': 4.597069597069597, '_deaths_per_hour': -2.033052059578721, 'targets_destroyed_per_hour': 0.8608058608058607, '_targets_destroyed_per_hour': -0.3506022781450866, 'vehicles_destroyed_per_hour': 3.241758241758242, '_vehicles_destroyed_per_hour': 0.8961623077850984, 'soldiers_healed_per_hour': 0.49450549450549447, '_soldiers_healed_per_hour': -0.04446001757721618, 'team_kills_per_hour': 1.7765567765567765, '_team_kills_per_hour': -0.46360195072635246, 'distance_moved_km_per_hour': 2.587912087912088, '_distance_moved_km_per_hour': -1.3015342726995964, 'shots_fired_per_hour': 922.1245421245421, '_shots_fired_per_hour': -868.340216785667, 'throwables_thrown_per_hour': 5.366300366300366, '_throwables_thrown_per_hour': -7.086880848301732, 'kills_per_km_moved': 162.30007077140834, '_kills_per_km_moved': 60.50368761454956, 'xp_per_shot_fired': 18.999880829427187, '_xp_per_shot_fired': 8.348826286977731, 'xp_per_kill': 41.71307722495966, '_xp_per_kill': 26.63358560589505, 'shots_fired_per_kill': 2.1954388871931276, '_shots_fired_per_kill': -6.018178890557561, 'team_kills_per_kill': 0.00422971264117211, '_team_kills_per_kill': -0.0052883238224496285, 'runs_around_the_equator': 0.0035258874625056307}
```
* Ranking a set of records between two dates returns an iterable of sqlalchemy.util.\_collections.result which are then printed (`_asdict()`) by rwrtrack 
  * *This is because diffing ranks uses the rwrtrack.rank.diffrank function which constructs, from the parameters, a SQL query where an `ORDER BY` is inserted for the specified metric.*
  * Example (debug) output that shows the constructed SQL statement:  
    ```
    (venv) PS C:\Users\david\projects\rwr\rwrtrack> .\rwrtrack.py -v rank xp_per_hour 20210525-20210813
    ...
    DEBUG: Executing stmt: 'SELECT ra.account_id AS account_id, ra.username AS username, ra.date AS ra_date, rb.date AS rb_date, ra.xp - rb.xp AS xp, ra.time_played - rb.time_played AS time_played, (ra.time_played - rb.time_played) / ? AS time_played_hours, ra.kills - rb.kills AS kills, ra.deaths - rb.deaths AS deaths, (ra.kills - rb.kills) - (ra.deaths - rb.deaths) AS score, ra.kill_streak - rb.kill_streak AS kill_streak, ra.targets_destroyed - rb.targets_destroyed AS targets_destroyed, ra.vehicles_destroyed - rb.vehicles_destroyed AS vehicles_destroyed, ra.soldiers_healed - rb.soldiers_healed AS soldiers_healed, ra.team_kills - rb.team_kills AS team_kills, ra.distance_moved - rb.distance_moved AS distance_moved, (ra.distance_moved - rb.distance_moved) / ? AS distance_moved_km, ra.shots_fired - rb.shots_fired AS shots_fired, ra.throwables_thrown - rb.throwables_thrown AS throwables_thrown, CAST(ra.kills - rb.kills AS FLOAT) / (ra.deaths - rb.deaths) AS kdr, CAST(ra.kills AS FLOAT) / ra.deaths - CAST(rb.kills AS FLOAT) / rb.deaths AS _kdr, (ra.xp - rb.xp) / ((ra.time_played - rb.time_played) / ?) AS xp_per_hour, ra.xp / (ra.time_played / ?) - rb.xp / (rb.time_played / ?) AS _xp_per_hour, (ra.kills - rb.kills) / ((ra.time_played - rb.time_played) / ?) AS kills_per_hour, ra.kills / (ra.time_played / ?) - rb.kills / (rb.time_played / ?) AS _kills_per_hour, (ra.deaths - rb.deaths) / ((ra.time_played - rb.time_played) / ?) AS deaths_per_hour, ra.deaths / (ra.time_played / ?) - rb.deaths / (rb.time_played / ?) AS _deaths_per_hour, (ra.targets_destroyed - rb.targets_destroyed) / ((ra.time_played - rb.time_played) / ?) AS targets_destroyed_per_hour, ra.targets_destroyed / (ra.time_played / ?) - rb.targets_destroyed / (rb.time_played / ?) AS _targets_destroyed_per_hour, (ra.vehicles_destroyed - rb.vehicles_destroyed) / ((ra.time_played - rb.time_played) / ?) AS vehicles_destroyed_per_hour, ra.vehicles_destroyed / (ra.time_played / ?) - rb.vehicles_destroyed / (rb.time_played / ?) AS _vehicles_destroyed_per_hour, (ra.soldiers_healed - rb.soldiers_healed) / ((ra.time_played - rb.time_played) / ?) AS soldiers_healed_per_hour, ra.soldiers_healed / (ra.time_played / ?) - rb.soldiers_healed / (rb.time_played / ?) AS _soldiers_healed_per_hour, (ra.team_kills - rb.team_kills) / ((ra.time_played - rb.time_played) / ?) AS team_kills_per_hour, ra.team_kills / (ra.time_played / ?) - rb.team_kills / (rb.time_played / ?) AS _team_kills_per_hour, ((ra.distance_moved - rb.distance_moved) / ?) / ((ra.time_played - rb.time_played) / ?) AS distance_moved_km_per_hour, (ra.distance_moved / ?) / (ra.time_played / ?) - (rb.distance_moved / ?) / (rb.time_played / ?) AS _distance_moved_km_per_hour, (ra.shots_fired - rb.shots_fired) / ((ra.time_played - rb.time_played) / ?) AS shots_fired_per_hour, ra.shots_fired / (ra.time_played / ?) - rb.shots_fired / (rb.time_played / ?) AS _shots_fired_per_hour, (ra.throwables_thrown - rb.throwables_thrown) / ((ra.time_played - rb.time_played) / ?) AS throwables_thrown_per_hour, ra.throwables_thrown / (ra.time_played / ?) - rb.throwables_thrown / (rb.time_played / ?) AS _throwables_thrown_per_hour, (ra.kills - rb.kills) / ((ra.distance_moved - rb.distance_moved) / ?) AS kills_per_km_moved, ra.kills / (ra.distance_moved / ?) - rb.kills / (rb.distance_moved / ?) AS _kills_per_km_moved, CAST(ra.xp - rb.xp AS FLOAT) / (ra.shots_fired - rb.shots_fired) AS xp_per_shot_fired, CAST(ra.xp AS FLOAT) / ra.shots_fired - CAST(rb.xp AS FLOAT) / rb.shots_fired AS _xp_per_shot_fired, CAST(ra.xp - rb.xp AS FLOAT) / (ra.kills - rb.kills) AS xp_per_kill, CAST(ra.xp AS FLOAT) / ra.kills - CAST(rb.xp AS FLOAT) / rb.kills AS _xp_per_kill, CAST(ra.shots_fired - rb.shots_fired AS FLOAT) / (ra.kills - rb.kills) AS shots_fired_per_kill, CAST(ra.shots_fired AS FLOAT) / ra.kills - CAST(rb.shots_fired AS FLOAT) / rb.kills AS _shots_fired_per_kill, CAST(ra.team_kills - rb.team_kills AS FLOAT) / (ra.kills - rb.kills) AS team_kills_per_kill, CAST(ra.team_kills AS FLOAT) / ra.kills - CAST(rb.team_kills AS FLOAT) / rb.kills AS _team_kills_per_kill, ((ra.distance_moved - rb.distance_moved) / ?) / ? AS runs_around_the_equator
    FROM records AS ra, records AS rb
    WHERE ra.account_id = rb.account_id AND ra.date = ? AND rb.date = ? ORDER BY xp_per_hour DESC
     LIMIT ? OFFSET ?'
    with parameters: '(60.0, 1000.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 1000.0, 60.0, 1000.0, 60.0, 1000.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 1000.0, 1000.0, 1000.0, 1000.0, 40075.017, 20210813, 20210525, 5, 0)'
    DEBUG: Execution took: 15.62ms
    [the results are rendered here :)]
    ```
  * That probably looks crazy but check out [difference.py](https://github.com/rwr-community-dev/rwrtrack/blob/master/rwrtrack/difference.py) if you want to see more about how it actually works - SqlAlchemy is magical 😁

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
