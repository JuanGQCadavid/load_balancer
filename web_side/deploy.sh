#!/bin/bash
echo "Cheking if docker is already installed"
if ! [ -x "$(command -v docker)" ]; then
  echo 'Docker is no isnatlled.'
  wget -qO- https://get.docker.com/ | sh
fi


echo "Building img"
docker build -t web-app-img .
echo "Done."
echo "Creating container for web app services..."
echo "[1] web app service running on port 80"
docker run -d --name web-app-service-1 -p 80:3333 web-app-img
echo "[1] Done.."
echo "[2] web app service running on port 5000"
docker run -d --name web-app-service-2 -p 5000:3333 web-app-img
echo "[2] Done.."