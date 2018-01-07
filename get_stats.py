import logging
import logging.config
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from stats import Stats, write_stats_to_csv


# script_dir = Path(__file__).parent
# log_conf_p = (script_dir / "logging.conf").resolve()
# log_p = (script_dir / "rwrtrack.log").resolve()
logger = logging.getLogger(__name__)
# logging.config.fileConfig(log_conf_p.as_posix(),
#                           disable_existing_loggers=False,
#                           defaults={"logfilename": log_p.as_posix()})
# logger.debug(f"Logging configured from {str(log_conf_p)}")
# logger.debug(f"Logging output will be written to {str(log_p)}")

playerstats_url = "http://rwr.runningwithrifles.com/rwr_stats/view_players.php"


def request_stats(start=0):
    logger.debug(f"Requesting stats ({start}-{start+100}) from server")
    url = f"{playerstats_url}?sort=rank_progression&start={start}"
    try:
        r = requests.get(url)
        r.raise_for_status()
        # Path("stats.html").write_text(r.text)
    except Exception as e:
        logger.critical(f"Requesting stats failed due to {type(e).__name__}",
                        exc_info=1)
        raise
    else:
        return r.text


def extract_rows(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table:
        rows = table.find_all("tr")[1::]
    return rows if rows else []


def convert_tp_to_mins(time_played):
    try:
        h, m = time_played.split(" ")
        hours = int(h[0:-1])
        mins = int(m[0:-3])
    except IndexError as e:
        logger.error(f"Converting {time_played} failed because of IndexError",
                     exc_info=1)
        raise
    except ValueError as e:
        logger.error(f"Converting {time_played} failed because of ValueError",
                     exc_info=1)
        raise
    else:
        return hours*60 + mins


def convert_dm_to_metres(distance_moved):
    # TODO: EXCEPTION HANDLING!
    dm_km = float(distance_moved[0:-2])
    dm_m = int(dm_km*1000)
    return dm_m


def extract_stats(row):
    cols = row.find_all("td")
    try:
        username = cols[1].get_text()
        kills = int(cols[2].get_text())
        deaths = int(cols[3].get_text())
        time_played = convert_tp_to_mins(cols[6].get_text())
        kill_streak = int(cols[7].get_text())
        targets_destroyed = int(cols[8].get_text())
        vehicles_destroyed = int(cols[9].get_text())
        soldiers_healed = int(cols[10].get_text())
        team_kills = int(cols[11].get_text())
        distance_moved = convert_dm_to_metres(cols[12].get_text())
        shots_fired = int(cols[13].get_text())
        throwables_thrown = int(cols[14].get_text())
        xp = int(cols[15].get_text())
    except IndexError as e:
        logger.error(f"Skipping row\n'{row}'\ndue to IndexError", exc_info=1)
        return None
    except ValueError as e:
        logger.error(f"Skipping row\n'{row}'\ndue to ValueError", exc_info=1)
        return None
    else:
        return Stats(username=username, xp=xp, time_played=time_played,
                     kills=kills, deaths=deaths, kill_streak=kill_streak,
                     targets_destroyed=targets_destroyed,
                     vehicles_destroyed=vehicles_destroyed,
                     soldiers_healed=soldiers_healed,
                     team_kills=team_kills,
                     distance_moved=distance_moved,
                     shots_fired=shots_fired,
                     throwables_thrown=throwables_thrown)


def get_stats(num_pages):
    logger.info(f"Retrieving {num_pages} page(s) of stats from server...")
    stats = []
    for x in range(0, num_pages*100, 100):
        html = request_stats(x)
        if html:
            rows = extract_rows(html)
            for row in rows:
                s = extract_stats(row)
                if s:
                    stats.append(s)
    return stats


def get_stats_test():
    # Hack function for developing new functionality without
    # hammering the RWR servers with requests
    logger.debug("Loading stats from stats.html example for testing")
    html = Path("stats.html").read_text(encoding="utf-8")
    stats = []
    if html:
        rows = extract_rows(html)
        for row in rows:
            s = extract_stats(row)
            stats.append(s)
    return stats
