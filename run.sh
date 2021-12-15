#!/bin/bash
export $(xargs < .env)

docker create \
	--name=jupyterhub_hub \
	--restart=unless-stopped \
	--network=${COMPOSE_PROJECT_NAME}_default \
	-v $DOCKER_SOCKET:/var/run/docker.sock \
	-v jupyterhub-data:/srv/jupyterhub \
	-v /data/i3home:/data/i3home \
	-v /data/i3store:/data/i3store \
	-v /scratch:/scratch \
	-v /cvmfs/icecube.opensciencegrid.org:/cvmfs/icecube.opensciencegrid.org \
	-e DOCKER_JUPYTER_IMAGE=icecube-jupyter \
	-e DOCKER_NETWORK_NAME=${COMPOSE_PROJECT_NAME}_default \
	-e DOCKER_JUPYTER_ADMINS=$JUPYTERHUB_ADMINS \
	-e DOCKER_JUPYTER_USERS=$JUPYTERHUB_USERS \
	-p $JUPYTERHUB_PORT:8000 \
	${JUPYTERHUB_IMAGE_REPOSITORY}:latest

docker start jupyterhub_hub
