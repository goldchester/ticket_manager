SELECT id, created_at, title FROM tickets
WHERE assigned_to = %s and status_id = 2 and solutions IS NOT NULL
ORDER BY
    CASE priority_id
        WHEN 1 THEN 1
        WHEN 2 THEN 2
        WHEN 3 THEN 3
        ELSE 4
    END,
    created_at;