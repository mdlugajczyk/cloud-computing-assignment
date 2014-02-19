import os
from neutronclient.neutron import client as neutron_client


class ApiClientFactory:

    @staticmethod
    def create_quantum_client():
        username = os.environ["OS_USERNAME"]
        tenant_name = os.environ["OS_TENANT_NAME"]
        password = os.environ["OS_PASSWORD"]
        auth_url = os.environ["OS_AUTH_URL"]
        region_name = os.environ["OS_REGION_NAME"]
        return neutron_client.Client("2.0", username=username,
                                     tenant_name=tenant_name,
                                     password="lassinesta",
                                     auth_url=auth_url,
                                     region_name=region_name)
