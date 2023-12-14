# Use the official MySQL base image
FROM mysql:latest

# Environment variables for MySQL
ENV MYSQL_ROOT_PASSWORD=password
ENV MYSQL_DATABASE=mysql01
#ENV MYSQL_USER=root
#ENV MYSQL_PASSWORD=password

# Expose the MySQL port
EXPOSE 3306

# Set the working directory
WORKDIR /usr/src/app

# (Optional) Copy custom MySQL configuration file
# COPY ./my.cnf /etc/mysql/my.cnf

# Copy SQL script to initialize the database
COPY ./init.sql /docker-entrypoint-initdb.d/

# Create a volume for MySQL data
VOLUME /var/lib/mysql

# Start MySQL service
CMD ["mysqld"]

