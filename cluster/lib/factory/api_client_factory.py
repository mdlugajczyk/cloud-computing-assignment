import os
from neutronclient.neutron import client as neutron_client
from novaclient.v1_1 import client as nova_client


class ApiClientFactory:

    def __init__(self):
        self._username = os.environ["OS_USERNAME"]
        self._tenant_name = os.environ["OS_TENANT_NAME"]
        self._password = os.environ["OS_PASSWORD"]
        self._auth_url = os.environ["OS_AUTH_URL"]
        self._region_name = os.environ["OS_REGION_NAME"]

    def create_quantum_client(self):
        return neutron_client.Client("2.0", username=self._username,
                                     tenant_name=self._tenant_name,
                                     password=self._password,
                                     auth_url=self._auth_url,
                                     region_name=self._region_name)

    def create_nova_client(self):
        return nova_client.Client(self._username, self._password,
                                  self._tenant_name, self._auth_url)

    def create_security_groups_manager(self):
        nova = self.create_nova_client()
        return nova.security_groups

    def create_security_rules_manager(self):
        nova = self.create_nova_client()
        return nova.security_group_rules

    def create_keypairs_manager(self):
        nova = self.create_nova_client()
        return nova.keypairs

    def create_servers_manager(self):
        nova = self.create_nova_client()
        return nova.servers

    def create_images_manager(self):
        nova = self.create_nova_client()
        return nova.images
