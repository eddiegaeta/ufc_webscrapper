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

# Create a cron job that runs every 5 minutes
# Redirect the cron job output to a log file
RUN (crontab -l ; echo "*/5 * * * * /usr/local/bin/python /app/webscrapper_ufc.py >> /var/log/cron.log 2>&1") | crontab -

# Run cron in the foreground
CMD ["cron", "-f"]

###Test
