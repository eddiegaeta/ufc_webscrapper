# Use Ubuntu as the base image
FROM ubuntu:18.04

# Install Python, cron, and other dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip cron build-essential libxml2-dev libxslt-dev libffi-dev libssl-dev mariadb-client python3-dev iputils-ping && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY webscrapper_ufc.py .

# Install additional dependencies for Beautiful Soup 4 and MySQL connector
RUN pip3 install beautifulsoup4 requests mysql-connector-python python-dotenv

# Create a cron job that runs every 5 minutes
# Redirect the cron job output to a log file
RUN (crontab -l ; echo "*/5 * * * * /usr/bin/python3 /app/webscrapper_ufc.py >> /var/log/cron.log 2>&1") | crontab -

# Run cron in the foreground
CMD ["cron", "-f"]

#Test
