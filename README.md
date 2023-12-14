# collection of code meant to build work flow for ufc.com webscrapping

## Docker image ...

# build docker container
docker build -t ufc_webscrapper .

# run docker conatainer
docker run ufc_webscrapper

# list docker container
docker ps| grep ufc

# exec into docker container
docker exec -it <containerid> /bin/ash

# review cronlogs
cat /var/logs/cron.log
