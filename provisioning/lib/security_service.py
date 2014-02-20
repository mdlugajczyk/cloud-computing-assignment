SSH_PORT = 22
ICMP_PORT = -1
TCP = "tcp"
ICMP = "icmp"
IP_RANGE = "0.0.0.0/0"

class SecurityService:

    def __init__(self, security_groups_manager, security_rules_manager):
        self._groups_manager = security_groups_manager
        self._rules_manager = security_rules_manager

    def setup_security(self):
        self._setup_ssh_rule()
        self._setup_ping_rule()

    def _setup_ping_rule(self):
        if (not self._ping_rule_exists()):
            self._create_rule(ICMP, ICMP_PORT)

    def _ping_rule_exists(self):
        return self._rule_exists(self._is_ping_rule)


    def _is_ping_rule(self, rule):
        return self._is_required_rule(rule, ICMP, ICMP_PORT)
        
    def _setup_ssh_rule(self):
        if (not self._ssh_rule_exists()):
            self._create_ssh_rule()

    def _ssh_rule_exists(self):
        return self._rule_exists(self._is_ssh_rule)

    def _is_ssh_rule(self, rule):
        return self._is_required_rule(rule, TCP, SSH_PORT)
            
    def _create_ssh_rule(self):
        self._create_rule(TCP, SSH_PORT)

    def _create_rule(self, protocol, port):
        default_group = self._default_secgroup()
        self._rules_manager.create(default_group.id,
                                   protocol_name=protocol,
                                   from_port=port,
                                   to_port=port,
                                   cidr=IP_RANGE)

    def _rule_exists(self, pred):
        default_group = self._default_secgroup()
        for rule in default_group.rules:
            if pred(rule):
                return True
        return False

    def _is_required_rule(self, rule, protocol, port):
        good_protocol = rule["ip_protocol"] == protocol
        good_from = rule["from_port"] == port
        good_to = rule["to_port"] == port
        good_range = rule["ip_range"] == {"cidr": IP_RANGE}
        return  good_protocol and good_from and good_to and good_range

    def _default_secgroup(self):
        for group in self._groups_manager.list():
            if group.name == "default":
                return group
