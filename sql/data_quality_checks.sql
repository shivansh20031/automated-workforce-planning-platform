-- Data Quality Checks for Workforce Planning Platform

-- 1. Check for duplicate employee IDs
SELECT 
    employee_id, 
    COUNT(*) AS record_count
FROM employees
GROUP BY employee_id
HAVING COUNT(*) > 1;

-- 2. Check for missing departments
SELECT *
FROM employees
WHERE department IS NULL;

-- 3. Check for invalid employment statuses
SELECT DISTINCT employment_status
FROM employees
WHERE employment_status NOT IN ('Active', 'Terminated');

-- 4. Check for employees without hashed IDs
SELECT *
FROM employees
WHERE hashed_employee_id IS NULL;

-- 5. Check for missing compensation records
SELECT e.employee_id
FROM employees e
LEFT JOIN compensation c
    ON e.employee_id = c.employee_id
WHERE c.employee_id IS NULL;

-- 6. Check for negative forecasted headcount
SELECT *
FROM headcount_forecast
WHERE forecasted_headcount < 0;