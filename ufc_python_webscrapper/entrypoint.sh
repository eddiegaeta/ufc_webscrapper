#!/bin/bash

# Export environment variables for cron
printenv | grep -v "no_proxy" >> /etc/environment

# Set up the cron job
(crontab -l ; echo "*/5 * * * * /usr/local/bin/python /app/webscrapper_ufc.py >> /var/log/cron.log 2>&1") | crontab -

# Start the cron daemon in the foreground
cron -f
