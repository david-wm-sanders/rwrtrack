class RenderTableMixin:
    def as_table(self):
        r = []
        # Make a beautiful table with box-drawing characters
        c0w = 20
        c1w = 12
        c2w = 10
        # Make the table header
        r.append(f"┌{'':─<{c0w}}┬{'':─<{c1w}}┬{'':─<{c2w}}┐")
        r.append(f"│{'Statistic':>{c0w}}"
                 f"│{'Value':>{c1w}}│{'per hour':>{c2w}}│")
        r.append(f"╞{'':═<{c0w}}╪{'':═<{c1w}}╪{'':═<{c2w}}╡")
        # Make basic statistics rows
        tph = self.time_played_hours
        r.append(f"│{'Time played in hours':>{c0w}}"
                 f"│{tph:>{c1w},.2f}│{'1':>{c2w}}│")
        r.append(f"│{'XP':>{c0w}}│{self.xp:>{c1w},}│{self.xp_ph:>{c2w},.2f}│")
        r.append(f"│{'Kills':>{c0w}}"
                 f"│{self.kills:>{c1w},}│{self.kills_ph:>{c2w}.2f}│")
        r.append(f"│{'Deaths':>{c0w}}"
                 f"│{self.deaths:>{c1w},}│{self.deaths_ph:>{c2w}.2f}│")
        td, tdph = self.targets_destroyed, self.targets_destroyed_ph
        r.append(f"│{'Targets destroyed':>{c0w}}"
                 f"│{td:>{c1w},}│{tdph:>{c2w}.2f}│")
        vd, vdph = self.vehicles_destroyed, self.vehicles_destroyed_ph
        r.append(f"│{'Vehicles destroyed':>{c0w}}"
                 f"│{vd:>{c1w},}│{vdph:>{c2w}.2f}│")
        sh, shph = self.soldiers_healed, self.soldiers_healed_ph
        r.append(f"│{'Soldiers healed':>{c0w}}"
                 f"│{sh:>{c1w},}│{shph:>{c2w}.2f}│")
        tk, tkph = self.team_kills, self.team_kills_ph
        r.append(f"│{'Team kills':>{c0w}}│{tk:>{c1w},}│{tkph:>{c2w}.2f}│")
        dm, dph = self.distance_moved_km, self.distance_moved_km_ph
        r.append(f"│{'Distance moved in km':>{c0w}}"
                 f"│{dm:>{c1w},.2f}│{dph:>{c2w}.2f}│")
        sf, sfph = self.shots_fired, self.shots_fired_ph
        r.append(f"│{'Shots fired':>{c0w}}│{sf:>{c1w},}│{sfph:>{c2w},.2f}│")
        tt, ttph = self.throwables_thrown, self.throwables_thrown_ph
        r.append(f"│{'Throwables thrown':>{c0w}}"
                 f"│{tt:>{c1w},}│{ttph:>{c2w}.2f}│")
        # Make a table break
        r.append(f"├{'':─<{c0w}}┼{'':─<{c1w}}┼{'':─<{c2w}}┤")
        # Make some derived statistics
        r.append(f"│{'Score':>{c0w}}│{self.score:>{c1w},}│{'-':>{c2w}}│")
        r.append(f"│{'K/D':>{c0w}}│{self.kdr:>{c1w}.2f}│{'-':>{c2w}}│")
        r.append(f"│{'XP per kill':>{c0w}}│"
                 f"{self.xp_pk:>{c1w},.2f}│{'-':>{c2w}}│")
        r.append(f"│{'XP per shot fired':>{c0w}}"
                 f"│{self.xp_pb:>{c1w},.2f}│{'-':>{c2w}}│")
        sf_pk = self.shots_fired_pk
        r.append(f"│{'Shots per kill':>{c0w}}"
                 f"│{sf_pk:>{c1w},.2f}│{'-':>{c2w}}│")
        tk_pk = self.team_kills_pk
        r.append(f"│{'Team kills per kill':>{c0w}}"
                 f"│{tk_pk:>{c1w},.5f}│{'-':>{c2w}}│")
        rate = self.runs_around_the_equator
        r.append(f"│{'Runs around equator':>{c0w}}"
                 f"│{rate:>{c1w}.5f}│{'-':>{c2w}}│")
        # Make the table footer
        r.append(f"╘{'':═<{c0w}}╧{'':═<{c1w}}╧{'':═<{c2w}}╛")

        return "\n".join(r)
