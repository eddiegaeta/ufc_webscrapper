# collection of code meant to build work flow for ufc.com webscrapping

## Docker image ...

# build docker container
sudo docker build -t ufc_scrapper_api .

# run docker conatainer
sudo docker run -d --name ufc_scrapper_api -p 3306:3306 -v mysql-data:/var/lib/mysql ufc_scrapper_api

# list docker container
sudo docker ps -a | grep ufc_scrapper_api
