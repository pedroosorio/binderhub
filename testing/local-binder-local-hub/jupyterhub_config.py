######################################################################
## A development config to test BinderHub locally.
#
# Run `jupyterhub --config=binderhub_config.py` terminal

# If True JupyterHub will take care of running BinderHub as a managed service
# If False then run `python3 -m binderhub -f binderhub_config.py` in another terminal
RUN_BINDERHUB_AS_JUPYTERHUB_SERVICE = True

# Host IP is needed in a few places
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
hostip = s.getsockname()[0]
s.close()

from binderhub.binderspawner_mixin import BinderSpawnerMixin
from dockerspawner import DockerSpawner
import os

# image & token are set via spawn options
class LocalContainerSpawner(BinderSpawnerMixin, DockerSpawner):
    pass


c.JupyterHub.spawner_class = LocalContainerSpawner
c.DockerSpawner.remove = True
c.LocalContainerSpawner.cmd = 'jupyter-notebook'

c.Application.log_level = 'DEBUG'
c.JupyterHub.Spawner.debug = True
c.JupyterHub.authenticator_class = "nullauthenticator.NullAuthenticator"

c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = hostip

binderhub_service_name = 'binder'
if RUN_BINDERHUB_AS_JUPYTERHUB_SERVICE:
    binderhub_config = os.path.join(os.path.dirname(__file__), 'binderhub_config.py')
    c.JupyterHub.services = [{
        "name": binderhub_service_name,
        "admin": True,
        "command": ["python", "-mbinderhub", f"--config={binderhub_config}"],
        "url": f"http://localhost:8585",
    }]
    c.JupyterHub.default_url = f"/services/{binderhub_service_name}/"
else:
    c.JupyterHub.services = [{
        "name": binderhub_service_name,
        "admin": True,
        "api_token": open(os.path.join(os.path.dirname(__file__), 'api_token.txt')).read(),
    }]
