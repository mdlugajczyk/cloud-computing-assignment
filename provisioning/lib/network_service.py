class NetworkService:

    def __init__(self, network_client):
        self._network_client = network_client
        self._network_id = None

    def setup_network(self):
        self._create_network()
        self._create_subnet()

    def _create_network(self):
        network = {"network": {"name": "s210664-assignment",
                               "admin_state_up": True}}
        response = self._network_client.create_network(network)
        self._network_id = response["network"]["id"]

    def _create_subnet(self):
        subnet = {"name": "s210664-assignment", "ip_version": "4",
                  "network_id": self._network_id,
                  "dns_nameservers": ["10.7.0.3"],
                  "cidr": "192.170.0.0/24"}
        self._network_client.create_subnet({"subnet": subnet})
