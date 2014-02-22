import unittest
from mockito import Mock, when, verify, any
from lib.open_stack_service.security import SecurityService
from novaclient.v1_1.security_groups import SecurityGroup

GROUP_ID = "group-id"
GROUP_NAME = "default"


class SecurityServiceTest(unittest.TestCase):

    def setUp(self):
        self._groups_manager = Mock()
        self._rules_manager = Mock()
        self._service = SecurityService(self._groups_manager,
                                        self._rules_manager)
        self._default_group = SecurityGroup("1", {"name": GROUP_NAME,
                                            "id": GROUP_ID, "rules": []})
        groups = [self._default_group]
        when(self._groups_manager).list().thenReturn(groups)
        
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
        
        
