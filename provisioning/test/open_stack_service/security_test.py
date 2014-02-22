import unittest
from mockito import Mock, when, verify, any
from mock import mock_open, patch
from novaclient.v1_1.security_groups import SecurityGroup
from novaclient.v1_1.keypairs import Keypair
from lib.open_stack_service.security import SecurityService
from lib.model.configuration import Configuration


GROUP_ID = "group-id"
GROUP_NAME = "default"
SSH_KEY = "ssh-key: random-public-key"


class SecurityServiceTest(unittest.TestCase):

    def setUp(self):
        self._configuration = Configuration()
        self._groups_manager = Mock()
        self._rules_manager = Mock()
        self._keys_manager = Mock()
        self._service = SecurityService(self._groups_manager,
                                        self._rules_manager,
                                        self._keys_manager,
                                        self._configuration)
        self._default_group = SecurityGroup("1", {"name": GROUP_NAME,
                                            "id": GROUP_ID, "rules": []})
        self._setup_ssh_key_file()
        groups = [self._default_group]
        when(self._groups_manager).list().thenReturn(groups)
        when(self._keys_manager).list().thenReturn([])

    def test_creates_security_rule_for_ssh(self):
        self._service.setup_security()
        verify(self._rules_manager).create(GROUP_ID, ip_protocol="tcp",
                                           from_port=22, to_port=22,
                                           cidr="0.0.0.0/0")

    def test_reuse_existing_ssh_rule(self):
        self._given_ssh_rule_exists()
        self._service.setup_security()

    def test_creates_security_rule_for_ping(self):
        self._service.setup_security()
        verify(self._rules_manager).create(GROUP_ID, ip_protocol="icmp",
                                           from_port=-1, to_port=-1,
                                           cidr="0.0.0.0/0")

    def test_reuse_existing_ping_rule(self):
        self._given_ping_rule_exists()
        self._service.setup_security()

    def test_adds_ssh_key(self):
        self._setup_security_with_mocked_file()
        key = self._configuration.ssh_key
        self._open_mocked.assert_called_once_with(key, 'r')
        verify(self._keys_manager).create(self._configuration.ssh_key_name,
                                          public_key=SSH_KEY)

    def test_reuse_existing_key(self):
        self._given_ssh_key_exists()
        self._setup_security_with_mocked_file()

    def _given_ssh_rule_exists(self):
        rules = [{'from_port': 22, 'group': {}, 'ip_protocol': 'tcp',
                  'to_port': 22,
                  'parent_group_id': GROUP_ID,
                  'ip_range': {'cidr': '0.0.0.0/0'},
                  'id': '33fa6d6a-b02e-46bf-bf70-5da83ddae144'}]
        self._default_group.rules = rules
        when(self._rules_manager).create(any(), ip_protocol="tcp",
                                         from_port=22, to_port=22,
                                         cidr=any()).thenRaise(Exception)

    def _given_ping_rule_exists(self):
        self._given_rule_exists("icmp", -1)

    def _given_rule_exists(self, protocol, port):
        rules = [{'from_port': port, 'group': {}, 'ip_protocol': protocol,
                  'to_port': port,
                  'parent_group_id': GROUP_ID,
                  'ip_range': {'cidr': '0.0.0.0/0'},
                  'id': '33fa6d6a-b02e-46bf-bf70-5da83ddae144'}]
        self._default_group.rules = rules
        when(self._rules_manager).create(any(), ip_protoco=protocol,
                                         from_port=port, to_port=port,
                                         cidr=any()).thenRaise(Exception)

    def _given_ssh_key_exists(self):
        when(self._keys_manager).create(self._configuration.ssh_key_name,
                                        public_key=SSH_KEY).thenRaise(Exception)
        keys = [Keypair(Mock(), {"name": "ssh key name"}),
                Keypair(Mock(), {"name": self._configuration.ssh_key_name})]
        when(self._keys_manager).list().thenReturn(keys)

    def _setup_ssh_key_file(self):
        self._open_name = 'lib.open_stack_service.security.open'
        self._open_mocked = mock_open(read_data=SSH_KEY)

    def _setup_security_with_mocked_file(self):
        with patch(self._open_name, self._open_mocked, create=True):
            self._service.setup_security()
