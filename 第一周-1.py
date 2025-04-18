CREATE DATABASE school;
USE school;
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    height DECIMAL(5,2)
);

INSERT INTO students (name, height) VALUES ('张三', 175.5);


SELECT * FROM students;

UPDATE students SET height = 180.0 WHERE name = '张三';

DELETE FROM students WHERE name = '张三';

