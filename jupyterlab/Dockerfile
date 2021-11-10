FROM icecube/icetray:combo-stable-tensorflow2.4.1-ubuntu20.04

ARG jl_version
ARG jh_version

RUN python3 -m pip install \
	jupyterlab==$jl_version \
	jupyterhub==$jh_version
