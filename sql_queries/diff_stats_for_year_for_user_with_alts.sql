SELECT GROUP_CONCAT(a.account_id) AS account_id, GROUP_CONCAT(a.username) AS username,
SUM(a.xp - b.xp) AS xp, SUM(a.time_played - b.time_played) AS time_played,
SUM(a.kills - b.kills) AS kills, SUM(a.deaths - b.deaths) AS deaths, SUM(a.kill_streak - b.kill_streak) AS kill_streak,
SUM(a.targets_destroyed - b.targets_destroyed) AS targets_destroyed, SUM(a.vehicles_destroyed - b.vehicles_destroyed) AS vehicles_destroyed,
SUM(a.soldiers_healed - b.soldiers_healed) AS soldiers_healed, SUM(a.team_kills - b.team_kills) AS team_kills,
SUM(a.distance_moved - b.distance_moved) / 1000.0 AS distance_moved_km, SUM(a.shots_fired - b.shots_fired) AS shots_fired
FROM records AS a, records AS b
WHERE a.username IN ("JFJFJFJFJFJF", "PRIVATE JF", "JF 2.0") AND a.date = 20191231 AND b.date = 20181231 AND a.account_id = b.account_id