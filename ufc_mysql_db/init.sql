CREATE DATABASE IF NOT EXISTS mysql01;
FLUSH PRIVILEGES;
USE mysql01;

CREATE USER 'mysqluser'@'%' IDENTIFIED WITH 'caching_sha2_password' BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'mysqluser'@'%';
FLUSH PRIVILEGES;

ALTER USER 'root'@'localhost' IDENTIFIED WITH 'caching_sha2_password' BY 'password';
GRANT ALL ON *.* TO 'root'@'localhost';

ALTER USER 'root'@'%' IDENTIFIED WITH 'caching_sha2_password' BY 'password';
GRANT ALL ON *.* TO 'root'@'%';

FLUSH PRIVILEGES;


