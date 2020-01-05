SELECT n.username, n.soldiers_healed - o.soldiers_healed as soldiers_healed
FROM records n, records o
WHERE n.date = 20191231 AND o.date = 20181231 AND n.account_id = o.account_id
ORDER BY soldiers_healed DESC