-- setup.sql

CREATE DATABASE IF NOT EXISTS todo_list_db;

USE todo_list_db;

-- Create a table for tasks
CREATE TABLE IF NOT EXISTS tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each task
    task_name VARCHAR(255) NOT NULL,         -- Task name/description
    status VARCHAR(50) DEFAULT 'Pending',    -- Task status: Pending, Completed, etc.
    due_date DATE,                           -- Due date for the task
    priority VARCHAR(50) DEFAULT 'Medium'    -- Priority: High, Medium, Low
);
-- Optionally, add some sample tasks for testing
INSERT INTO tasks (task_name, status, due_date, priority)
VALUES
    ('Complete the SQL setup', 'Pending', '2024-10-30', 'High'),
    ('Study for the programming exam', 'Pending', '2024-11-01', 'Medium'),
    ('Start SQL project', 'Completed', '2024-10-20', 'Low');