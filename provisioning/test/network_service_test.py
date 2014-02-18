import unittest
from network_service import NetworkService
from mockito import Mock, verify, when


class NetworkServiceTest(unittest.TestCase):

    def setUp(self):
        self._setup_client()
        self._service = NetworkService(self._client)

    def test_creates_network(self):
        self._service.setup_network()
        network = {"network": {"name": "s210664-assignment",
                               "admin_state_up": True}}
        verify(self._client).create_network(network)

    def test_creates_subnet(self):
        self._service.setup_network()
        subnet = {"name": "s210664-assignment", "ip_version": "4",
                  "network_id": "c51a9627-dd94-4f0e-91d2-fe5ac5cf3e73",
                  "dns_nameservers": ["10.7.0.3"]}
        verify(self._client).create_subnet({"subnet": subnet})

    def _setup_client(self):
        self._client = Mock()
        network_created = {u'status': u'ACTIVE', u'subnets': [],
                           u'name': u'dupa', u'admin_state_up': True,
                           u'tenant_id':
                           u'5df84b0d2e4f48468824415146c684e5',
                           u'router:external': False, u'shared': False,
                           u'id': u'c51a9627-dd94-4f0e-91d2-fe5ac5cf3e73'}
        response = {"network": network_created}
        network = {"network": {"name": "s210664-assignment",
                   "admin_state_up": True}}
        when(self._client).create_network(network).thenReturn(response)
