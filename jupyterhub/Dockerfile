ARG version

FROM jupyterhub/jupyterhub:${version}

ARG version
ARG ds_version

# Copy the JupyterHub configuration in the container
COPY jupyterhub_config.py .

# Install dependencies (for advanced authentication and spawning)
RUN pip install \
	dockerspawner==$ds_version \
	jupyterhub-idle-culler
