import os
import sys
import docker
import sshauthenticator

from dockerspawner import DockerSpawner
from jupyter_client.localinterfaces import public_ips


def get_options_form(spawner):
    return options_form_tpl.format(default_image=spawner.image)


def set_nb_user(spawner):
    spawner.environment['NB_USER'] = spawner.user.name


class CustomDockerSpawner(DockerSpawner):
    def options_from_form(self, formdata):
        options = {}
        image_form_list = formdata.get("image", [])
        if image_form_list and image_form_list[0]:
            options["image"] = image_form_list[0].strip()
            self.log.info(f"User selected image: {options['image']}")
        return options

    def load_user_options(self, options):
        image = options.get("image")
        if image:
            self.log.info(f"Loading image {image}")
            self.image = image


images = []
with open('images.txt', 'r') as f:
    images = f.readlines()

options_form_tpl = '\n'.join([
    '<label for="image">Image</label>',
    '<select name="image" class="form-control" placeholder="the image to launch (default: {default_image})">',
    *[f'\t<option value={image}>{image}</option>' for image in images],
    '</select>'
])

admins = os.environ['DOCKER_JUPYTER_ADMINS']
if admins == '':
    admins = set()
else:
    admins = set(admins.replace(' ', '').split(','))

users = os.environ['DOCKER_JUPYTER_USERS']
if users == '':
    users = set()
else:
    users = set(users.replace(' ', '').split(','))

c.JupyterHub.spawner_class = CustomDockerSpawner
c.CustomDockerSpawner.options_form = get_options_form
c.CustomDockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
c.CustomDockerSpawner.prefix = 'jupyter_testing'
c.CustomDockerSpawner.pre_spawn_hook = set_nb_user

# Redirect to JupyterLab, instead of the plain Jupyter notebook
c.Spawner.default_url = '/lab'

c.CustomDockerSpawner.environment = {
    'SHELL': '/bin/bash',
    'GRANT_SUDO': '1',
    'CHOWN_HOME': '1',
    'NB_GID': '100',
}

# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
c.DockerSpawner.notebook_dir = notebook_dir 
c.DockerSpawner.volumes = {
    'jupyterhub-user-{username}': notebook_dir,
    '/data/i3store/': '/data/i3store',
    '/data/i3home/{username}': '/data/i3home/{username}',
    '/scratch/users/{username}': '/scratch/users/{username}',
    '/cvmfs/icecube.opensciencegrid.org': '/cvmfs/icecube.opensciencegrid.org',
}

# spawn containers that can access the gpus
c.DockerSpawner.extra_host_config = {
    "device_requests": [
        docker.types.DeviceRequest(
            count=-1,
            capabilities=[["gpu"]],
        ),
    ],
}

# user data persistence
c.JupyterHub.authenticator_class = 'sshauthenticator.SSHAuthenticator'
c.SSHAuthenticator.admin_users = admins
c.SSHAuthenticator.allowed_users = users
c.SSHAuthenticator.server_address = 'pa-pub.umd.edu'
c.SSHAuthenticator.server_port = 22

c.JupyterHub.hub_ip = public_ips()[0]

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

