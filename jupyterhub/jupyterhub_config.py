import os
import sys
import docker

from jupyter_client.localinterfaces import public_ips

ip = public_ips()[0]
print("IPS!!!")
print(ip)

c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'

#c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.hub_ip = ip

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_IMAGE']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
c.JupyterHub.hub_ip = os.environ['HUB_IP']

# Uncomment for jupyterhub version >= 2.0 
# c.JupyterHub.load_roles = [
#     {
#         "name": "jupyterhub-idle-culler-role",
#         "scopes": [
#             "list:users",
#             "read:users:activity",
#             "read:servers",
#             "delete:servers",
#             # "admin:users", # if using --cull-users
#         ],
#         # assignment of role's permissions to:
#         "services": ["jupyterhub-idle-culler-service"],
#     }
# ]

c.JupyterHub.services = [
    {
        "name": "jupyterhub-idle-culler-service",
        "command": [
            sys.executable,
            "-m", "jupyterhub_idle_culler",
            "--timeout=3600",
        ],
        "admin": True, # Comment out for jupyterhub version >= 2.0
    }
]

# Redirect to JupyterLab, instead of the plain Jupyter notebook
c.Spawner.default_url = '/lab'

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

# spawn containers that can access the gpus
c.DockerSpawner.extra_host_config = {
    "device_requests": [
        docker.types.DeviceRequest(
            count=-1,
            capabilities=[["gpu"]],
        ),
    ],
}
