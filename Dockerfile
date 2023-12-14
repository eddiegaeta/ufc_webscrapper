
######################
# Use Alpine Linux as the base image
FROM python:3.8-alpine

# Install any dependencies your script may need
RUN apk add --no-cache build-base libxml2-dev libxslt-dev

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY webscrapper_ufc.py .

# Install additional dependencies for Beautiful Soup 4 and MySQL connector
RUN apk add --no-cache libffi-dev openssl-dev mariadb-dev

# Install beautifulsoup4, requests, and mysql-connector using pip
RUN pip install beautifulsoup4 requests mysql-connector-python

# Create a cron job that runs every 5 minutes
# Redirect the cron job output to a log file
RUN echo "*/5 * * * * /usr/local/bin/python /app/webscrapper_ufc.py >> /var/log/cron.log 2>&1" | crontab -

# Run the cron daemon in the foreground
CMD ["crond", "-f"]
