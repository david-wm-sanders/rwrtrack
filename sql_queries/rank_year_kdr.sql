SELECT n.username, CAST(n.kills - o.kills AS FLOAT) / (n.deaths - o.deaths) as kdr
FROM records n, records o
WHERE n.date = 20191231 AND o.date = 20181231 AND n.account_id = o.account_id
ORDER BY kdr DESC