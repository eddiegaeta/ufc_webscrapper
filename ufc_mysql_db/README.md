# collection of code meant to build work flow for ufc.com webscrapping

## local docker image builds

### build docker container
`sudo docker build -t mysql01 .`

### run docker conatainer
`sudo docker run -d --name mysql01 -p 3306:3306 -v mysql-data:/var/lib/mysql --env-file .env mysql01`

### join docker network
`sudo docker network connect dev_network mysql01`

### list docker container
`sudo docker ps -a | grep mysql01`

### verify environmental variables in container
`sudo docker exec mysql01 env`

---

## remote docker image builds

### 




