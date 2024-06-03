SELECT 
    e.dep AS department_id
FROM 
    employees e
JOIN 
    departments d ON e.dep = d.id
WHERE 
    e.id = %s;