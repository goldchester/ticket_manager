DELETE FROM departments;
INSERT INTO departments (name) VALUES ('IT'), ('HR'), ('Finances');

DELETE FROM employees;
INSERT INTO employees (name, surname, dep) VALUES ('Mihailo', 'Yanovskyi', '1'), 
('Petro', 'Giganovich', '1'), ('Dmitro', 'Lantanovich', '1'), ('Henry', 'Wrigh', '2'), 
('Booby', 'Bricks', '2'), ('Merry', 'Jane', '3'), ('Jack', 'Slickback', '3');

DELETE FROM priority;
INSERT INTO priority (name) VALUES ('High'), ('Default'), ('Low');

DELETE FROM status;
INSERT INTO status (name) VALUES ('New'), ('Being solved'), ('Solved');