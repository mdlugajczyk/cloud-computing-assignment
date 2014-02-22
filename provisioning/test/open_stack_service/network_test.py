import unittest
from lib.open_stack_service.network import NetworkService
from mockito import Mock, verify, when, any


NETWORK_ID = "5df84b0d2e4f48468824415146c684e5"
NETWORK_NAME = "s210664-assignment-net"
SUBNET_NAME = "s210664-assignment-subnet"

class NetworkServiceTest(unittest.TestCase):

    def setUp(self):
        self._setup_client()
        self._service = NetworkService(self._client)

    def test_creates_network(self):
        self._service.setup_network()
        self._verify_creates_network()

    def test_creates_subnet_with_network_id(self):
        self._service.setup_network()
        self._verify_creates_subnet_with_network_id()

    def test_reuse_network(self):
        self._given_network_already_exists()
        self._service.setup_network()
        self._verify_creates_subnet_with_network_id()

    def test_reuse_subnet(self):
        self._given_subnet_already_exists()
        self._service.setup_network()

    def _setup_client(self):
        self._client = Mock()
        network_created = {u'status': u'ACTIVE', u'subnets': [],
                           u'name': u'dupa', u'admin_state_up': True,
                           u'tenant_id':
                           u'5df84b0d2e4f48468824415146c684e5',
                           u'router:external': False, u'shared': False,
                           u'id': NETWORK_ID}
        response = {"network": network_created}
        network = {"network": {"name": NETWORK_NAME,
                   "admin_state_up": True}}
        when(self._client).create_network(network).thenReturn(response)
        when(self._client).list_networks().thenReturn({"networks": []})
        when(self._client).list_subnets().thenReturn({"subnets": []})

    def _verify_creates_subnet_with_network_id(self):
        subnet = {"name": SUBNET_NAME, "ip_version": "4",
                  "network_id": NETWORK_ID,
                  "dns_nameservers": ["10.7.0.3"],
                  "cidr": "192.170.0.0/24"}
        verify(self._client).create_subnet({"subnet": subnet})

    def _given_network_already_exists(self):
        networks = {u'status': u'ACTIVE',
                    u'subnets': [u'495075eb-d0af-4cb2-945d-c0a60325c969'],
                    u'name': NETWORK_NAME, u'admin_state_up': True,
                    u'tenant_id': u'5df84b0d2e4f48468824415146c684e5',
                    u'router:external': False, u'shared': False, u'id':
                    NETWORK_ID}
        when(self._client).list_networks().thenReturn({"networks":
                                                       [networks]})
        when(self._client).create_network(any()).thenRaise(Exception)

    def _verify_creates_network(self):
        network = {"network": {"name": NETWORK_NAME,
                               "admin_state_up": True}}
        verify(self._client).create_network(network)

    def _given_subnet_already_exists(self):
        subnets = [{'name': SUBNET_NAME, 'enable_dhcp': True,
                    'network_id': 'a1f26172-88ab-42de-b63d-e8cf22f8c5af',
                    'tenant_id': '5df84b0d2e4f48468824415146c684e5',
                    'dns_nameservers': ['10.7.0.3'],
                    'allocation_pools': [{'start': '192.170.0.2',
                                          'end': '192.170.0.254'}],
                    'host_routes': [], 'ip_version': 4,
                    'gateway_ip': '192.170.0.1', 'cidr': '192.170.0.0/24',
                    'id': '495075eb-d0af-4cb2-945d-c0a60325c969'}]
        when(self._client).list_subnets().thenReturn({"subnets": subnets})
        when(self._client).create_subnet(any()).thenRaise(Exception)
        
        