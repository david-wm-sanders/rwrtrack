from collections import defaultdict
from stats_offline import load_stats

def load_kcs(kc_string):
    kcs = defaultdict(int)
    kc_counts = kc_string.split(",")
    for kc_count in kc_counts:
        combo, count = kc_count.split(":")
        combo, count = int(combo), int(count)
        if count:
            kcs[combo] = count
    return kcs

def kc_session(stats):
    penult, last = stats[-2], stats[-1]
    penult_kcs = load_kcs(penult.kill_combos)
    last_kcs = load_kcs(last.kill_combos)
    kcs_change = defaultdict(int)
    for combo in last_kcs:
        change = last_kcs[combo] - penult_kcs[combo]
        if change:
            kcs_change[combo] = change
    sesh_combos = ", ".join([f"{k}:{v}" for k, v in kcs_change.items()])
    print(f"Sesh: Combos: {sesh_combos}")

if __name__ == '__main__':
    stats = load_stats()
    kc_session(stats)
