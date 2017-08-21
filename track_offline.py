import csv
import xml.etree.ElementTree as etree
from datetime import datetime, timezone
from pathlib import Path

csv_path = Path("stats_offline.csv")
profile_path = Path.home() / "AppData\Roaming\Running with rifles\summary_profile.xml"

field_headers = ["utc", "tp", "gv", "k", "d", "tk", "ks", "td", "vd", "sh", "dm", "sf", "tt", "rp", "ds", "kc"]

if not csv_path.exists():
    with csv_path.open("w", newline="") as csv_file:
        print("Creating stats.csv and writing CSV field headers...")
        writer = csv.writer(csv_file)
        writer.writerow(field_headers)

with profile_path.open() as profile_file:
    print("Processing summary_profile.xml...")
    profile_xml = profile_file.read()
    profile = etree.fromstring(profile_xml)
    stats_element = profile.find("stats")
    stats = stats_element.attrib
    utc = datetime.now(timezone.utc)
    tp = int(float(stats["time_played"]))
    gv = profile.attrib["game_version"]
    k = stats["kills"]
    d = stats["deaths"]
    tk = stats["teamkills"]
    ks = stats["longest_kill_streak"]
    td = stats["targets_destroyed"]
    vd = stats["vehicles_destroyed"]
    sh = stats["soldiers_healed"]
    dm = stats["distance_moved"]
    sf = stats["shots_fired"]
    tt = stats["throwables_thrown"]
    rp = stats["rank_progression"]
    ds = -1
    kc = -1
    monitor_elements = stats_element.findall("monitor")
    for monitor_element in monitor_elements:
        monitor = monitor_element.attrib
        if "name" in monitor:
            if monitor["name"] == "death streak":
                ds = monitor["longest_death_streak"]
            elif monitor["name"] == "kill combo":
                kill_combos_d = {}
                entry_elements = monitor_element.findall("entry")
                for entry_element in entry_elements:
                    entry = entry_element.attrib
                    kill_combos_d[int(entry["combo"])] = int(entry["count"])
                kill_combos = []
                x = 3
                while True:
                    if x in kill_combos_d:
                        c = kill_combos_d[x]
                        kill_combos.append(f"{x}:{c}")
                        x += 1
                    else:
                        break
                kc = ",".join(kill_combos)
            else:
                print(f"""Monitor '{monitor["name"]}' not processed.""")

    # print(f"utc={utc}, tp={tp}, gv={gv}, k={k}, d={d}, tk={tk}, ks={ks}, td={td}, vd={vd}, sh={sh}, dm={dm}, sf={sf}, tt={tt}, rp={rp}, ds={ds}, kc={kc}")

    with csv_path.open("r+", newline="") as csv_file:
        csvd = csv_file.readlines()
        last_tp, last_k, last_d = None, None, None
        last_row = [csvd[0], csvd[-1]]
        reader = csv.DictReader(last_row)
        for row in reader:
            try:
                last_tp = int(row["tp"])
                last_k = int(row["k"])
                last_d = int(row["d"])
            except ValueError:
                # csv.DictReader outputs the field name row if no other rows exist,
                # so catch the VaueErrors that occur if int is passed a string, e.g. "tp"
                pass
        tp_changed = True if not last_tp or tp > last_tp else False
        k_changed = True if not last_k or int(k) > last_k else False
        d_changed = True if not last_d or int(d) > last_d else False
        if tp_changed and (k_changed or d_changed):
            print("Updating stats.csv")
            writer = csv.writer(csv_file)
            writer.writerow([utc, tp, gv, k, d, tk, ks, td, vd, sh, dm, sf, tt, rp, ds, kc])
        else:
            print("No significant changes in summary_profile.xml since stats_offline.csv was last updated")
