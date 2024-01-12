# Collection of code meant to build work flow for ufc.com webscrapping

## local docker image builds

### build docker container
`docker build -t ufc_webscrapper .`

### run docker container
`docker run --env-file .env --name ufc_webscrapper ufc_webscrapper`

### join docker network
`docker network connect dev_network ufc_webscrapper`

### list docker container
`docker ps| grep ufc`

### exec into docker container
`docker exec -it ufc_webscrapper /bin/bash`

### review cronlogs
`cat /var/log/cron.log`

### verify environmental variables in container
`docker exec ufc_webscrapper env`

---

## remote docker image builds

### 