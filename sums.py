from datetime import date
from pathlib import Path

from stats import load_stats_from_csv


# Approximate equatorial circumference of Earth
earth_equat_circumference = 40075  # km


def print_analysis(num_rows_summed, xp, tp, k, d, td, vd, sh, dm, sf, tt):
    # Convert some stats to more useful forms
    tp_hours = tp / 60
    dm_km = dm / 1000

    # Print sums with basic conversions for time_played and distance_moved
    print(f"Number of rows summed: {num_rows_summed}")
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


def sum_stats_and_analyse(stats, output_at_rows):
    xp, tp, k, d, td, vd, sh, dm, sf, tt = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for i, s in enumerate(stats, 1):
        xp += s.xp
        tp += s.time_played
        k += s.kills
        d += s.deaths
        td += s.targets_destroyed
        vd += s.vehicles_destroyed
        sh += s.soldiers_healed
        dm += s.distance_moved
        sf += s.shots_fired
        tt += s.throwables_thrown

        if i in output_at_rows:
            print_analysis(i, xp, tp, k, d, td, vd, sh, dm, sf, tt)


if __name__ == '__main__':
    csv_hist_path = Path(__file__).parent / Path("csv_historical")
    csv_files = sorted(list(csv_hist_path.glob("*.csv")), reverse=True)
    most_recent_csv_file = csv_files[0]
    print(f"Loading {most_recent_csv_file.name}...\n\n")
    stats = load_stats_from_csv(most_recent_csv_file)
    output_at_rows = [5, 10, 25, 50, 100, 250, 500, 750, 1000]
    sum_stats_and_analyse(stats, output_at_rows)
