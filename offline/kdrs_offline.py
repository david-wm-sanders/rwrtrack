from stats_offline import load_stats

def kdr_session(stats):
    a, b = stats[-1], stats[-2]
    k = a.kills - b.kills
    d = a.deaths - b.deaths
    tk = a.team_kills - b.team_kills
    sh = a.soldiers_healed - b.soldiers_healed
    try:
        kdr = k / d
    except ZeroDivisionError:
        kdr = k
    print(f"Sesh: Kills: {k:6}, Deaths: {d:6}, KDR: {kdr:6.1f}, " \
          f"Soldiers healed: {sh:6}, Team kills: {tk:5}")

def kdr_life(stats):
    k, d = stats[-1].kills, stats[-1].deaths
    sh, tk = stats[-1].soldiers_healed, stats[-1].team_kills
    try:
        kdr = k / d
    except ZeroDivisionError:
        kdr = k
    print(f"Life: Kills: {k:6}, Deaths: {d:6}, KDR: {kdr:6.2f}, " \
          f"Soldiers healed: {sh:6}, Team kills: {tk:5}")

def kdr_record(stats):
    first, last, penult = stats[0], stats[-1], stats[-2]
    k = last.kills - first.kills
    d = last.deaths - first.deaths
    try:
        kdr = k / d
    except ZeroDivisionError:
        kdr = k
    k2 = penult.kills - first.kills
    d2 = penult.deaths - first.deaths
    try:
        kdr2 = k2 / d2
    except ZeroDivisionError:
        kdr2 = k2
    kdrc = kdr - kdr2
    print(f"Recd: Kills: {k:6}, Deaths: {d:6}, KDR: {kdr:6.2f}, {'Previous:'.rjust(16)} {kdr2:6.2f}, {'Change:'.rjust(11)} {kdrc:+5.2f}")

if __name__ == '__main__':
    stats = load_stats()
    kdr_session(stats)
    kdr_life(stats)
    kdr_record(stats)
