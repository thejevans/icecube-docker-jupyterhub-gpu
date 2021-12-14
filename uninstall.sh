#!/bin/bash
export $(xargs < .env)

basedir=jupyterlab-images
prefix=$JUPYTERLAB_IMAGE_PREFIX
repository=$JUPYTERLAB_IMAGE_REPOSITORY

# remove jupyterlab dockerfiles
[ -d "${basedir}" ] && rm -r ${basedir}

# remove docker images
while read p; do
  image=${prefix}-${p##*:}
  docker rmi ${repository}:${image}
done < images.txt
