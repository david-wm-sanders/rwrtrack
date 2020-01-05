SELECT n.username, n.kills - o.kills as kills
FROM records n, records o
WHERE n.date = 20191231 AND o.date = 20181231 AND n.account_id = o.account_id
ORDER BY kills DESC