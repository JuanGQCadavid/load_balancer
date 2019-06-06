#!/bin/bash
docker build -t load-balancer-img .
docker run -d --name load-balancer-service -p 80:9000 load-balancer-img
