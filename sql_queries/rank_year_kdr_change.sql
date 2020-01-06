SELECT n.username, CAST(n.kills AS FLOAT) / n.deaths - CAST(o.kills AS FLOAT) / o.deaths as kdr_diff
FROM records n, records o
WHERE n.date = 20191231 AND o.date = 20181231 AND n.account_id = o.account_id
ORDER BY kdr_diff DESC