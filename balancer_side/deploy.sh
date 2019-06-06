#!/bin/bash
echo "Cheking if docker is already installed"
if ! [ -x "$(command -v docker)" ]; then
  echo 'Docker is no isnatlled.'
  wget -qO- https://get.docker.com/ | sh
fi

echo "Building load balancer image ..."
docker build -t load-balancer-img .
echo "Done."
echo "Staring service load balancer at port 80 ..."
docker run -d --name load-balancer-service -p 80:9000 load-balancer-img
echo "Done."