SELECT records.username AS username, records.time_played AS time_played, records.kills AS kills, records.team_kills AS team_kills, CASE WHEN (records.kills > 0) THEN CAST(records.team_kills AS FLOAT) / records.kills ELSE 0 END AS team_kills_per_kill
FROM records
WHERE records.date = 20191231 ORDER BY team_kills_per_kill DESC
LIMIT 10 OFFSET 0
