#!/bin/bash

docker stop jupyterhub_hub
docker rm jupyterhub_hub
docker volume rm jupyterhub-data
docker stop $(docker ps -a --format '{{.Names}}' | grep jupyter_testing)
docker rm $(docker ps -a --format '{{.Names}}' | grep jupyter_testing)
