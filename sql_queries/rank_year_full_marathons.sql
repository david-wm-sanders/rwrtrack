SELECT n.username, (n.distance_moved - o.distance_moved) / 1000.0 as distance_moved_km, (n.distance_moved - o.distance_moved) / 42195.0 as full_marathons
FROM records n, records o
WHERE n.date = 20191231 AND o.date = 20181231 AND n.account_id = o.account_id
ORDER BY distance_moved_km DESC