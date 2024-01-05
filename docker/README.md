# collection of code meant to build work flow for ufc.com webscrapping

## Docker network ...

# build docker network to ensure hostname resolution

docker network create dev_network

# join containers to the same network

docker network connect dev_network mysql01
docker network connect dev_network ufc_webscrapper
docker network connect dev_network ufc_scrapper_api






