SELECT
    t.id AS ticket_id,
    t.title AS ticket_title,
    t.created_at,
    t.problem,
    t.solved_at,
    t.solutions,
    e1.name AS created_by_name,
    e1.surname AS created_by_surname,
    e2.name AS assigned_to_name,
    e2.surname AS assigned_to_surname,
    d1.name AS created_by_department,
    d2.name AS assigned_to_department,
    p.name AS priority,
    s.name AS status
FROM
    tickets t
LEFT JOIN
    employees e1 ON t.created_by_id = e1.id
LEFT JOIN
    employees e2 ON t.assigned_to = e2.id
LEFT JOIN
    departments d1 ON e1.dep = d1.id
LEFT JOIN
    departments d2 ON t.assigned_to_dep = d2.id
LEFT JOIN
    priority p ON t.priority_id = p.id
LEFT JOIN
    status s ON t.status_id = s.id
WHERE
    t.assigned_to = %s
ORDER BY
    CASE t.priority_id
        WHEN 1 THEN 1
        WHEN 2 THEN 2
        WHEN 3 THEN 3
        ELSE 4
    END,
    t.created_at;
