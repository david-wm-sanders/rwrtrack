import sys
from pathlib import Path

from stats import load_stats_from_csv, stats_to_dict


# Approximate equatorial circumference of Earth
earth_equat_circumference = 40075  # km


def print_analysis(s):
    # Print a beautiful table with box-drawing characters
    c0w = 20
    cw = 10
    # Draw the table header
    print(f"┌{'':─<{c0w}}┬{'':─<{cw}}┬{'':─<{cw}}┐")
    print(f"│{'Statistic':<{c0w}}│{'Value':>{cw}}│{'per hour':>{cw}}│")
    print(f"╞{'':═<{c0w}}╪{'':═<{cw}}╪{'':═<{cw}}╡")
    # Draw the statistics rows
    tph = s.time_played_hours
    print(f"│{'Time played in hours':>{c0w}}│{tph:>{cw}.2f}│{'-':>{cw}}│")
    print(f"│{'XP':>{c0w}}│{s.xp:>{cw}}│{s.xp_ph:>{cw}.2f}│")
    print(f"│{'Kills':>{c0w}}│{s.kills:>{cw}}│{s.kills_ph:>{cw}.2f}│")
    print(f"│{'Deaths':>{c0w}}│{s.deaths:>{cw}}│{s.deaths_ph:>{cw}.2f}│")
    print(f"│{'K/D':>{c0w}}│{s.kdr:>{cw}.2f}│{'-':>{cw}}│")
    td, tdph = s.targets_destroyed, s.targets_destroyed_ph
    print(f"│{'Targets destroyed':>{c0w}}│{td:>{cw}}│{tdph:>{cw}.2f}│")
    vd, vdph = s.vehicles_destroyed, s.vehicles_destroyed_ph
    print(f"│{'Vehicles destroyed':>{c0w}}│{vd:>{cw}}│{vdph:>{cw}.2f}│")
    sh, shph = s.soldiers_healed, s.soldiers_healed_ph
    print(f"│{'Soldiers healed':>{c0w}}│{sh:>{cw}}│{shph:>{cw}.2f}│")
    dm, dmph = s.distance_moved_km, s.distance_moved_km_ph
    print(f"│{'Distance moved in km':>{c0w}}│{dm:>{cw}.2f}│{dmph:>{cw}.2f}│")
    rate = s.distance_moved_km / earth_equat_circumference
    print(f"│{'Runs around equator':>{c0w}}│{rate:>{cw}.5f}│{'-':>{cw}}│")
    sf, sfph = s.shots_fired, s.shots_fired_ph
    print(f"│{'Shots fired':>{c0w}}│{sf:>{cw}}│{sfph:>{cw}.2f}│")
    tt, ttph = s.throwables_thrown, s.throwables_thrown_ph
    print(f"│{'Throwables thrown':>{c0w}}│{tt:>{cw}}│{ttph:>{cw}.2f}│")
    # Print the table footer
    print(f"└{'':─<{c0w}}┴{'':─<{cw}}┴{'':─<{cw}}┘")


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
    print_analysis(ps)
