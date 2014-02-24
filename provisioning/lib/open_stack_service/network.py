NETWORK_NAME = "s210664-assignment-net"
SUBNET_NAME = "s210664-assignment-subnet"


class NetworkService:

    def __init__(self, network_client):
        self._network_client = network_client
        self._network_id = None

    def assign_ip(self, server):
        port_id = self._port_id_for_server(server.id)
        public_network = self._public_network_id()
        self._create_ip_for_port_in_network(port_id, public_network)

    def setup_network(self):
        self._setup_network()
        self._setup_subnet()
        self._setup_router()
        return self._network_id

    def _create_ip_for_port_in_network(self, port_id, network_id):
        create_ip_request = {"floatingip": {"floating_network_id": network_id,
                                            "port_id": port_id}}
        self._network_client.create_floatingip(create_ip_request)

    def _public_network_id(self):
        networks = self._get_networks()
        public_network = self._record_with_name(networks, 'public')
        return public_network['id']
        
    def _port_id_for_server(self, server_id):
        ports_request = {"device_id": server_id}
        ports = self._network_client.list_ports()['ports']
        return next(p['id'] for p in ports if p['device_id'] == server_id)

    def _setup_network(self):
        if (not self._network_exists(NETWORK_NAME)):
            self._create_network()

    def _create_network(self):
        network = {"network": {"name": NETWORK_NAME,
                               "admin_state_up": True}}
        response = self._network_client.create_network(network)
        self._network_id = response["network"]["id"]

    def _network_exists(self, network_name):
        networks = self._get_networks()
        network = self._record_with_name(networks, network_name)
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
        subnet = self._record_with_name(subnets, SUBNET_NAME)
        if subnet:
            self._subnet_id = subnet['id']
            return True
        else:
            return False

    def _create_subnet(self):
        subnet = {"name": "s210664-assignment-subnet", "ip_version": "4",
                  "network_id": self._network_id,
                  "dns_nameservers": ["10.7.0.3"],
                  "cidr": "192.170.0.0/24"}
        response = self._network_client.create_subnet({"subnet": subnet})
        self._subnet_id = response['subnet']['id']

    def _setup_router(self):
        self._create_router()
        self._set_router_gateway()
        self._set_router_interface()

    def _create_router(self):
        router = {"router": {"name": "s210664-router"}}
        created_router = self._network_client.create_router(router)
        self._router_id = created_router['router']['id']

    def _set_router_gateway(self):
        public_network = self._find_public_network()
        network = {"network_id": public_network['id']}
        self._network_client.add_gateway_router(self._router_id, network)

    def _set_router_interface(self):
        subnet = {"subnet_id": self._subnet_id}
        self._network_client.add_interface_router(self._router_id,
                                                  subnet)

    def _record_with_name(self, collection, name):
        return next((r for r  in collection if r['name'] == name), None)

    def _find_public_network(self):
        return self._record_with_name(self._get_networks(),
                                      "public")
    def _get_networks(self):
        return self._network_client.list_networks()['networks']
