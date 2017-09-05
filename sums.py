from datetime import date
from pathlib import Path

from stats import load_stats_from_csv


# Approximate equatorial circumference of Earth
earth_equat_circumference = 40075  # km


def sum_stats_and_analyse(stats):
    xp, tp, k, d, td, vd, sh, dm, sf, tt = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for s in stats:
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
    # print(xp, tp, k, d, td, vd, sh, dm, sf, tt)

    # Convert some stats to more useful forms
    tp_hours = tp / 60
    dm_km = dm / 1000

    # Print sums with basic conversions for time_played and distance_moved
    print(f"Number of rows summed: {len(stats)}")
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


if __name__ == '__main__':
    d = date(2017, 9, 3)
    p = Path(__file__).parent / Path(f"csv_historical/{d}.csv")
    stats = load_stats_from_csv(p)
    sum_stats_and_analyse(stats)
