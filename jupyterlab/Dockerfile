FROM icecube/icetray:combo-stable-tensorflow2.4.1-ubuntu20.04

ARG jl_version
ARG jh_version

# jupyterhub requires npm and nodejs
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update \
 && apt-get install -yq --no-install-recommends \
	npm \
	nodejs \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# jupyterhub needs to be installed on spawned containers
RUN python3 -m pip install \
	jupyterlab==$jl_version \
	jupyterhub==$jh_version
