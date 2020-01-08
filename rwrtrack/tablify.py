def render_table(data):
    r = []
    # Make a beautiful table with box-drawing characters
    c0w = 20
    c1w = 12
    c2w = 10

    # Make the table header.
    r.append(f"┌{'':─<{c0w}}┬{'':─<{c1w}}┬{'':─<{c2w}}┐")
    # Make the table column headers
    r.append(f"│{'Statistic':>{c0w}}"
             f"│{'Value':>{c1w}}│{'per hour':>{c2w}}│")
    r.append(f"╞{'':═<{c0w}}╪{'':═<{c1w}}╪{'':═<{c2w}}╡")
    # Make basic statistics rows
    tph = data.time_played_hours
    r.append(f"│{'Time played in hours':>{c0w}}"
             f"│{tph:>{c1w},.2f}│{'1':>{c2w}}│")
    r.append(f"│{'XP':>{c0w}}│{data.xp:>{c1w},}│{data.xp_per_hour:>{c2w},.2f}│")
    r.append(f"│{'Kills':>{c0w}}"
             f"│{data.kills:>{c1w},}│{data.kills_per_hour:>{c2w}.2f}│")
    r.append(f"│{'Deaths':>{c0w}}"
             f"│{data.deaths:>{c1w},}│{data.deaths_per_hour:>{c2w}.2f}│")
    td, tdph = data.targets_destroyed, data.targets_destroyed_per_hour
    r.append(f"│{'Targets destroyed':>{c0w}}"
             f"│{td:>{c1w},}│{tdph:>{c2w}.2f}│")
    vd, vdph = data.vehicles_destroyed, data.vehicles_destroyed_per_hour
    r.append(f"│{'Vehicles destroyed':>{c0w}}"
             f"│{vd:>{c1w},}│{vdph:>{c2w}.2f}│")
    sh, shph = data.soldiers_healed, data.soldiers_healed_per_hour
    r.append(f"│{'Soldiers healed':>{c0w}}"
             f"│{sh:>{c1w},}│{shph:>{c2w}.2f}│")
    tk, tkph = data.team_kills, data.team_kills_per_hour
    r.append(f"│{'Team kills':>{c0w}}│{tk:>{c1w},}│{tkph:>{c2w}.2f}│")
    dm, dph = data.distance_moved_km, data.distance_moved_km_per_hour
    r.append(f"│{'Distance moved in km':>{c0w}}"
             f"│{dm:>{c1w},.2f}│{dph:>{c2w}.2f}│")
    sf, sfph = data.shots_fired, data.shots_fired_per_hour
    r.append(f"│{'Shots fired':>{c0w}}│{sf:>{c1w},}│{sfph:>{c2w},.2f}│")
    tt, ttph = data.throwables_thrown, data.throwables_thrown_per_hour
    r.append(f"│{'Throwables thrown':>{c0w}}"
             f"│{tt:>{c1w},}│{ttph:>{c2w}.2f}│")
    # Make a table break
    r.append(f"├{'':─<{c0w}}┼{'':─<{c1w}}┼{'':─<{c2w}}┤")
    # Make some derived statistics
    r.append(f"│{'Score':>{c0w}}│{data.score:>{c1w},}│{'-':>{c2w}}│")
    r.append(f"│{'K/D':>{c0w}}│{data.kdr:>{c1w}.2f}│{'-':>{c2w}}│")
    r.append(f"│{'Kills per km':>{c0w}}"
             f"│{data.kills_per_km_moved:>{c1w},.2f}│{'-':>{c2w}}│")
    r.append(f"│{'XP per shot fired':>{c0w}}"
             f"│{data.xp_per_shot_fired:>{c1w},.2f}│{'-':>{c2w}}│")
    r.append(f"│{'XP per kill':>{c0w}}│"
             f"{data.xp_per_kill:>{c1w},.2f}│{'-':>{c2w}}│")
    sf_per_kill = data.shots_fired_per_kill
    r.append(f"│{'Shots per kill':>{c0w}}"
             f"│{sf_per_kill:>{c1w},.2f}│{'-':>{c2w}}│")
    tk_per_kill = data.team_kills_per_kill
    r.append(f"│{'Team kills per kill':>{c0w}}"
             f"│{tk_per_kill:>{c1w},.5f}│{'-':>{c2w}}│")
    r.append(f"│{'Runs around equator':>{c0w}}"
             f"│{data.runs_around_the_equator:>{c1w}.5f}│{'-':>{c2w}}│")
    # Make the table footer
    r.append(f"╘{'':═<{c0w}}╧{'':═<{c1w}}╧{'':═<{c2w}}╛")

    print("\n".join(r))
