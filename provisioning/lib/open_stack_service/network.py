NETWORK_NAME = "s210664-assignment-net"
SUBNET_NAME = "s210664-assignment-subnet"


class NetworkService:

    def __init__(self, network_client):
        self._network_client = network_client
        self._network_id = None

    def setup_network(self):
        self._setup_network()
        self._setup_subnet()

    def _setup_network(self):
        if (not self._network_exists()):
            self._create_network()

    def _create_network(self):
        network = {"network": {"name": NETWORK_NAME,
                               "admin_state_up": True}}
        response = self._network_client.create_network(network)
        self._network_id = response["network"]["id"]

    def _network_exists(self):
        networks = self._network_client.list_networks()['networks']
        for network in networks:
            if network['name'] == NETWORK_NAME:
                self._network_id = network['id']
                return True
        return False

    def _setup_subnet(self):
        if (not self._subnet_exists()):
            self._create_subnet()

    def _subnet_exists(self):
        subnets = self._network_client.list_subnets()['subnets']
        for subnet in subnets:
            if subnet['name'] == SUBNET_NAME:
                return True
        return False

    def _create_subnet(self):
        subnet = {"name": "s210664-assignment-subnet", "ip_version": "4",
                  "network_id": self._network_id,
                  "dns_nameservers": ["10.7.0.3"],
                  "cidr": "192.170.0.0/24"}
        self._network_client.create_subnet({"subnet": subnet})
