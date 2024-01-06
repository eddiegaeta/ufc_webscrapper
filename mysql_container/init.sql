
CREATE DATABASE IF NOT EXISTS mysql01;
FLUSH PRIVILEGES;
USE mysql01;

CREATE USER 'mysqluser'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'mysqluser'@'%';
FLUSH PRIVILEGES;

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
GRANT ALL ON *.* TO 'root'@'localhost';

ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
GRANT ALL ON *.* TO 'root'@'%';

FLUSH PRIVILEGES;


