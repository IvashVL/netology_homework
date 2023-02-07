DROP TABLE IF EXISTS employee;

CREATE TABLE IF NOT EXISTS employee (
	employee_id INT PRIMARY KEY,
	employee_name TEXT NOT NULL,
	department TEXT NOT NULL,
	head INT REFERENCES employee
);