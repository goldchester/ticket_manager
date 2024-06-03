SELECT id, created_at, problem, title, assigned_to_dep, priority_id FROM tickets
WHERE created_by_id = %s and status_id <> 3
ORDER BY
    CASE priority_id
        WHEN 1 THEN 1
        WHEN 2 THEN 2
        WHEN 3 THEN 3
        ELSE 4
    END,
    created_at;