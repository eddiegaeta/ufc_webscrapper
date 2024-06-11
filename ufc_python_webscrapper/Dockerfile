# Use Python 3.8 as the base image
FROM python:3.8-slim

# Install cron and other dependencies
RUN apt-get update && \
    apt-get install -y cron build-essential libxml2-dev libxslt-dev libffi-dev libssl-dev mariadb-client iputils-ping && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script and requirements file into the container
COPY webscrapper_ufc.py .
COPY requirements.txt .

# Install additional dependencies for Beautiful Soup 4 and MySQL connector
RUN pip install -r requirements.txt

# Copy the entrypoint script into the container
COPY entrypoint.sh /usr/local/bin/

# Make the entrypoint script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Define the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
