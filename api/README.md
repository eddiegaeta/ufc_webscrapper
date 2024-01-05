# collection of code meant to build work flow for ufc.com webscrapping

## Docker image ...

# build docker container
docker build -t ufc_scrapper_api .

# run docker conatainer
docker run -d --name ufc_scrapper_api -p 3000:3000 --env-file .env ufc_scrapper_api

# join docker network
sudo docker network connect dev_network ufc_scrapper_api

# list docker container
docker ps -a | grep ufc_scrapper_api

# verify environmental variables in container
docker exec ufc_scrapper_api env 
