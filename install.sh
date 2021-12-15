#!/bin/bash
export $(xargs < .env)

basedir=jupyterlab-images
prefix=$JUPYTERLAB_IMAGE_PREFIX
repository=$JUPYTERLAB_IMAGE_REPOSITORY

# Copy images.txt to jupyterhub directory
cp images.txt ./jupyterhub
sed -i "s|.*:|${repository}:${prefix}-|g" ./jupyterhub/images.txt

# Build dockerfiles for each image in images.txt
[ ! -d "${basedir}" ] && mkdir ${basedir}
while read p; do
  image=${prefix}-${p##*:}
  dir=${basedir}/${image}
  [ ! -d "${dir}" ] && mkdir ${dir}
  cp Dockerfile.template ${dir}/Dockerfile
  sed -i "s|%%IMAGE%%|$p|g" ${dir}/Dockerfile
done < images.txt

# Create docker network and volume for jupyterhub
docker volume create --name jupyterhub-data
docker network create ${COMPOSE_PROJECT_NAME}_default

# Build jupyterhub image
docker build \
	-t ${JUPYTERHUB_IMAGE_REPOSITORY}:latest \
	--build-arg version=$JUPYTERHUB_VERSION \
	--build-arg ds_version=$DOCKERSPAWNER_VERSION \
	./jupyterhub

# Build docker images from each dockerfile
while read p; do
  image=${prefix}-${p##*:}
  dir=${basedir}/${image}
  tag=${repository}:${image}
  docker build \
    -t ${tag} \
    --build-arg jh_version=$JUPYTERHUB_VERSION \
    --build-arg jl_version=$JUPYTERLAB_VERSION \
    ./${dir}
done < images.txt
