SELECT 
    d.name AS department_name,
    CONCAT(e.name, ' ', e.surname) AS full_name,
    e.id AS emp_id,
    d.id AS department_id
FROM 
    employees e
JOIN 
    departments d ON e.dep = d.id;