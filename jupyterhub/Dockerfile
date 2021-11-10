ARG version

FROM jupyterhub/jupyterhub:${version}

ARG ds_version

# Copy the JupyterHub configuration in the container
COPY jupyterhub_config.py .

# Install dependencies (for advanced authentication and spawning)
RUN pip install \
	jupyter_client \
	dockerspawner==$ds_version \
	jupyterhub-idle-culler
