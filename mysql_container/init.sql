CREATE DATABASE IF NOT EXISTS mysql01;

USE mysql01;

-- CREATE USER 'mysql_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
-- GRANT ALL PRIVILEGES ON *.* TO 'mysql_user'@'localhost' WITH GRANT OPTION;
-- CREATE USER 'mysql_user'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
-- GRANT ALL PRIVILEGES ON *.* TO 'mysql_user'@'%' WITH GRANT OPTION;
-- GRANT ALL PRIVILEGES ON *.* TO 'mysql_user' WITH GRANT OPTION;

-- FLUSH PRIVILEGES;


ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
GRANT ALL ON *.* TO 'root'@'localhost';
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
GRANT ALL ON *.* TO 'root'@'%';
GRANT ALL ON *.* TO 'root';

FLUSH PRIVILEGES;

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;


