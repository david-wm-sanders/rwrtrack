import logging
import sys
from pathlib import Path

from .stats_csv import load_stats_from_csv, stats_list_to_dict


logger = logging.getLogger(__name__)


def print_analysis(s):
    # Print a beautiful table with box-drawing characters
    c0w = 20
    c1w = 12
    c2w = 10
    # Print the table header
    print(f"┌{'':─<{c0w}}┬{'':─<{c1w}}┬{'':─<{c2w}}┐")
    print(f"│{'Statistic':>{c0w}}│{'Value':>{c1w}}│{'per hour':>{c2w}}│")
    print(f"╞{'':═<{c0w}}╪{'':═<{c1w}}╪{'':═<{c2w}}╡")
    # Print basic statistics rows
    tph = s.time_played_hours
    print(f"│{'Time played in hours':>{c0w}}│{tph:>{c1w},.2f}│{'1':>{c2w}}│")
    print(f"│{'XP':>{c0w}}│{s.xp:>{c1w},}│{s.xp_ph:>{c2w},.2f}│")
    print(f"│{'Kills':>{c0w}}│{s.kills:>{c1w},}│{s.kills_ph:>{c2w}.2f}│")
    print(f"│{'Deaths':>{c0w}}│{s.deaths:>{c1w},}│{s.deaths_ph:>{c2w}.2f}│")
    td, tdph = s.targets_destroyed, s.targets_destroyed_ph
    print(f"│{'Targets destroyed':>{c0w}}│{td:>{c1w},}│{tdph:>{c2w}.2f}│")
    vd, vdph = s.vehicles_destroyed, s.vehicles_destroyed_ph
    print(f"│{'Vehicles destroyed':>{c0w}}│{vd:>{c1w},}│{vdph:>{c2w}.2f}│")
    sh, shph = s.soldiers_healed, s.soldiers_healed_ph
    print(f"│{'Soldiers healed':>{c0w}}│{sh:>{c1w},}│{shph:>{c2w}.2f}│")
    tk, tkph = s.team_kills, s.team_kills_ph
    print(f"│{'Team kills':>{c0w}}│{tk:>{c1w},}│{tkph:>{c2w}.2f}│")
    dm, dph = s.distance_moved_km, s.distance_moved_km_ph
    print(f"│{'Distance moved in km':>{c0w}}│{dm:>{c1w},.2f}│{dph:>{c2w}.2f}│")
    sf, sfph = s.shots_fired, s.shots_fired_ph
    print(f"│{'Shots fired':>{c0w}}│{sf:>{c1w},}│{sfph:>{c2w},.2f}│")
    tt, ttph = s.throwables_thrown, s.throwables_thrown_ph
    print(f"│{'Throwables thrown':>{c0w}}│{tt:>{c1w},}│{ttph:>{c2w}.2f}│")
    # Print a table break
    print(f"├{'':─<{c0w}}┼{'':─<{c1w}}┼{'':─<{c2w}}┤")
    # Print some derived statistics
    print(f"│{'Score':>{c0w}}│{s.score:>{c1w},}│{'-':>{c2w}}│")
    print(f"│{'K/D':>{c0w}}│{s.kdr:>{c1w}.2f}│{'-':>{c2w}}│")
    print(f"│{'XP per kill':>{c0w}}│{s.xp_pk:>{c1w},.2f}│{'-':>{c2w}}│")
    print(f"│{'XP per shot fired':>{c0w}}│{s.xp_pb:>{c1w},.2f}│{'-':>{c2w}}│")
    sf_pk = s.shots_fired_pk
    print(f"│{'Shots per kill':>{c0w}}│{sf_pk:>{c1w},.2f}│{'-':>{c2w}}│")
    tk_pk = s.team_kills_pk
    print(f"│{'Team kills per kill':>{c0w}}│{tk_pk:>{c1w},.5f}│{'-':>{c2w}}│")
    rate = s.runs_around_the_equator
    print(f"│{'Runs around equator':>{c0w}}│{rate:>{c1w}.5f}│{'-':>{c2w}}│")
    # Print the table footer
    print(f"╘{'':═<{c0w}}╧{'':═<{c1w}}╧{'':═<{c2w}}╛")


# def print_individual_analysis(stats_dict, name):
#     logger.info(f"Finding '{name}'...")
#     try:
#         ps = stats_dict[name]
#         print_analysis(ps)
#     except KeyError as e:
#         logger.error(f"'{name}' not found...")
#         sys.exit(1)
