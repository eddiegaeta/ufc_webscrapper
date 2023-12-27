# collection of code meant to build work flow for ufc.com webscrapping

## Docker image ...

# build docker container
sudo docker build -t mysql01 .

# run docker conatainer
sudo docker run -d --name mysql01 -p 3306:3306 -v mysql-data:/var/lib/mysql mysql01

# list docker container
sudo docker ps -a | grep mysql01
