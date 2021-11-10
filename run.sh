#!/bin/bash
export $(xargs < .env)

docker volume create --name jupyterhub-data
docker network create ${COMPOSE_PROJECT_NAME}_default

docker build \
	-t jupyterhub \
	--build-arg version=$JUPYTERHUB_VERSION \
	--build-arg ds_version=$DOCKERSPAWNER_VERSION \
	./jupyterhub

docker build \
	-t icecube-jupyter \
	--build-arg jh_version=$JUPYTERHUB_VERSION \
	--build-arg jl_version=$JUPYTERLAB_VERSION \
	./jupyterlab

docker create \
	--name=jupyterhub_hub \
	--restart=unless-stopped \
	-v $DOCKER_SOCKET:/var/run/docker.sock \
	-v jupyterhub-data:/srv/jupyterhub \
	-e DOCKER_JUPYTER_IMAGE=icecube-jupyter \
	-e DOCKER_NETWORK_NAME=${COMPOSE_PROJECT_NAME}_default \
	-e HUB_IP=jupyterhub_hub \
	-p $JUPYTERHUB_PORT:8000 \
	jupyterhub

docker start jupyterhub_hub
