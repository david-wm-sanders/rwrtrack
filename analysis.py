import sys
from pathlib import Path

from stats import load_stats_from_csv, stats_to_dict


# Approximate equatorial circumference of Earth
earth_equat_circumference = 40075  # km


def calculate_metrics(s):
    # Calculate some derived stats and stick them back into the SimpleNamespace
    s.time_played_hours = s.time_played / 60
    s.distance_moved_km = s.distance_moved / 1000

    s.kdr = s.kills / s.deaths

    s.xp_ph = s.xp / s.time_played_hours
    s.kills_ph = s.kills / s.time_played_hours
    s.deaths_ph = s.deaths / s.time_played_hours
    s.targets_destroyed_ph = s.targets_destroyed / s.time_played_hours
    s.vehicles_destroyed_ph = s.vehicles_destroyed / s.time_played_hours
    s.soldiers_healed_ph = s.soldiers_healed / s.time_played_hours
    s.distance_moved_km_ph = s.distance_moved_km / s.time_played_hours
    s.shots_fired_ph = s.shots_fired / s.time_played_hours
    s.throwables_thrown_ph = s.throwables_thrown / s.time_played_hours

    s.runs_around_the_equator = s.distance_moved_km / earth_equat_circumference


def print_analysis(s):
    # Print values
    print(f"XP: {s.xp}")
    print(f"Time played: {s.time_played_hours:.2f} hours")
    print(f"Kills: {s.kills}")
    print(f"Deaths: {s.deaths}")
    print(f"Targets destroyed: {s.targets_destroyed}")
    print(f"Vehicles destroyed: {s.vehicles_destroyed}")
    print(f"Soldiers healed: {s.soldiers_healed}")
    print(f"Distance moved: {s.distance_moved_km:.2f}km")
    print(f"Shots fired: {s.shots_fired}")
    print(f"Throwables thrown: {s.throwables_thrown}")

    # Print derived per hour statistics
    print("\nDerived \"per hour\" statistics:")
    print(f"XP per hour: {s.xp_ph:.2f}")
    print(f"Kills per hour: {s.kills_ph:.2f}")
    print(f"Deaths per hour: {s.deaths_ph:.2f}")
    print(f"Targets destroyed per hour: {s.targets_destroyed_ph:.2f}")
    print(f"Vehicles destroyed per hour: {s.vehicles_destroyed_ph:.2f}")
    print(f"Soldiers healed per hour: {s.soldiers_healed_ph:.2f}")
    print(f"Distance moved per hour: {s.distance_moved_km_ph:.2f}km")
    print(f"Shots fired per hour: {s.shots_fired_ph:.2f}")
    print(f"Throwables thrown per hour: {s.throwables_thrown_ph:.2f}")

    # Print some other statistics
    print("\nDerived statistics:")
    print(f"K/D: {s.kdr:.2f}")
    print(f"Runs around the equator: {s.runs_around_the_equator:.5f}")
    print("\n")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: analysis.py NAME or analysis.py \"NAME WITH SPACES\"")
        sys.exit(1)
    name = sys.argv[1].upper()
    csv_hist_path = Path(__file__).parent / Path("csv_historical")
    csv_files = sorted(list(csv_hist_path.glob("*.csv")), reverse=True)
    most_recent_csv_file = csv_files[0]
    print(f"Loading {most_recent_csv_file.name}...")
    stats_list = load_stats_from_csv(most_recent_csv_file)
    stats = stats_to_dict(stats_list)
    print(f"Finding '{name}'...")
    try:
        ps = stats[name]
    except KeyError as e:
        print(f"'{name}' not found in {most_recent_csv_file.name}")
        sys.exit(1)

    calculate_metrics(ps)
    print_analysis(ps)