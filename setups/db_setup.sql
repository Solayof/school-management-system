DROP DATABASE IF EXISTS school_db;
CREATE DATABASE IF NOT EXISTS school_db;
DROP DATABASE IF EXISTS test_db;
CREATE DATABASE IF NOT EXISTS test_db;
CREATE USER IF NOT EXISTS 'school_admin'@'localhost' IDENTIFIED BY 'arisekola';
GRANT ALL ON `school_db`.* TO 'school_admin'@'localhost';
GRANT ALL ON `test_db`.* TO 'school_admin'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'school_admin'@'localhost';
FLUSH PRIVILEGES;
