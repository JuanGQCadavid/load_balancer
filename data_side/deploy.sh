#!/bin/bash
echo "Cheking if docker is already installed"
if ! [ -x "$(command -v docker)" ]; then
  echo 'Docker is no isnatlled.'
  wget -qO- https://get.docker.com/ | sh
fi

docker volume create mysql-db-data
docker volume ls
docker run -d -p 33060:3306 --name app-mysql-db -e MYSQL_ROOT_PASSWORD=soylaclavesecreta --mount src=mysql-db-data,dst=/var/lib/mysql mysql
docker exec -it app-mysql-db mysql -p