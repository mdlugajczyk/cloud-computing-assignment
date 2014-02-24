NETWORK_NAME = "s210664-assignment-net"
SUBNET_NAME = "s210664-assignment-subnet"


class NetworkService:

    def __init__(self, network_client):
        self._network_client = network_client
        self._network_id = None

    def setup_network(self):
        self._setup_network()
        self._setup_subnet()
        self._setup_router()
        return self._network_id

    def _setup_network(self):
        if (not self._network_exists()):
            self._create_network()

    def _create_network(self):
        network = {"network": {"name": NETWORK_NAME,
                               "admin_state_up": True}}
        response = self._network_client.create_network(network)
        self._network_id = response["network"]["id"]

    def _network_exists(self):
        networks = self._get_networks()
        network = self._record_with_name(networks, NETWORK_NAME)
        if network:
            self._network_id = network['id']
            return True
        else:
            return False

    def _setup_subnet(self):
        if (not self._subnet_exists()):
            self._create_subnet()

    def _subnet_exists(self):
        subnets = self._network_client.list_subnets()['subnets']
        return self._record_with_name(subnets, SUBNET_NAME) != None

    def _create_subnet(self):
        subnet = {"name": "s210664-assignment-subnet", "ip_version": "4",
                  "network_id": self._network_id,
                  "dns_nameservers": ["10.7.0.3"],
                  "cidr": "192.170.0.0/24"}
        self._network_client.create_subnet({"subnet": subnet})

    def _setup_router(self):
        self._create_router()
        self._set_router_gateway()

    def _create_router(self):
        router = {"router": {"name": "s210664-router"}}
        created_router = self._network_client.create_router(router)
        self._router_id = created_router['router']['id']

    def _set_router_gateway(self):
        public_network = self._find_public_network()
        network = {"network_id": public_network['id']}
        self._network_client.add_gateway_router(self._router_id, network)

    def _record_with_name(self, collection, name):
        for record in collection:
            if record['name'] == name:
                return record

    def _find_public_network(self):
        return self._record_with_name(self._get_networks(),
                                      "public")
    def _get_networks(self):
        return self._network_client.list_networks()['networks']
