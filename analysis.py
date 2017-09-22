import sys
from pathlib import Path

from stats import load_stats_from_csv, stats_to_dict


# Approximate equatorial circumference of Earth
earth_equat_circumference = 40075  # km


def print_analysis(xp, tp, k, d, td, vd, sh, dm, sf, tt):
    # Convert some stats to more useful forms
    tp_hours = tp / 60
    dm_km = dm / 1000

    # Print sums with basic conversions for time_played and distance_moved
    print(f"XP: {xp}")
    print(f"Time played: {tp_hours:.2f} hours")
    print(f"Kills: {k}")
    print(f"Deaths: {d}")
    print(f"Targets destroyed: {td}")
    print(f"Vehicles destroyed: {vd}")
    print(f"Soldiers healed: {sh}")
    print(f"Distance moved: {dm_km:.2f}km")
    print(f"Shots fired: {sf}")
    print(f"Throwables thrown: {tt}")

    # Print derived per hour statistics
    print("\nDerived \"per hour\" statistics:")
    print(f"XP per hour: {xp/tp_hours:.2f}")
    print(f"Kills per hour: {k/tp_hours:.2f}")
    print(f"Deaths per hour: {d/tp_hours:.2f}")
    print(f"Targets destroyed per hour: {td/tp_hours:.2f}")
    print(f"Vehicles destroyed per hour: {vd/tp_hours:.2f}")
    print(f"Soldiers healed per hour: {sh/tp_hours:.2f}")
    print(f"Distance moved per hour: {dm_km/tp_hours:.2f}km")
    print(f"Shots fired per hour: {sf/tp_hours:.2f}")
    print(f"Throwables thrown per hour: {tt/tp_hours:.2f}")

    # Print some derived other statistics
    print("\nDerived statistics:")
    print(f"Average K/D: {k/d:.2f}")
    print(f"Runs around the equator: {dm_km/earth_equat_circumference:.2f}")
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

    print_analysis(ps.xp, ps.time_played, ps.kills, ps.deaths,
                   ps.targets_destroyed, ps.vehicles_destroyed,
                   ps.soldiers_healed, ps.distance_moved,
                   ps.shots_fired, ps.throwables_thrown)
