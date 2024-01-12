# collection of code meant to build work flow for ufc.com webscrapping

## Docker image ...

# build docker container
sudo docker build -t ufc_webscrapper .

# run docker container
sudo docker run --env-file .env --name ufc_webscrapper ufc_webscrapper

# join docker network
sudo docker network connect dev_network ufc_webscrapper

# list docker container
sudo docker ps| grep ufc

# exec into docker container
sudo docker exec -it ufc_webscrapper /bin/bash

# review cronlogs
cat /var/log/cron.log

# verify environmental variables in container
sudo docker exec ufc_webscrapper env 

