# collection of code meant to build work flow for ufc.com webscrapping

## Docker image ...

# build docker container
sudo docker build -t mysql .

# run docker conatainer
sudo docker run -d --name mysql -p 3306:3306 -v mysql-data:/var/lib/mysql mysql

# list docker container
sudo docker ps -a | grep mysql
