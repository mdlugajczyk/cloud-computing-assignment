import unittest
import logging
from lib.service.cluster_builder import ClusterBuilder
from mockito import Mock, when, verify

class ClusterBuilderTest(unittest.TestCase):

    def setUp(self):
        self._factory = Mock()
        self._given_security_service()
        self._given_network_service()
        self._given_servers_service()
        self._given_node_checker()
        self._given_file_generator()
        self._logger = Mock()
        self._builder = ClusterBuilder(self._factory, self._logger)        

    def test_creates_network(self):
        self._builder.build_cluster()
        verify(self._network).setup_network()

    def test_creates_security(self):
        self._builder.build_cluster()
        verify(self._security).setup_security()

    def test_boots_vms(self):
        self._builder.build_cluster()
        verify(self._servers).boot_servers(10, self._network_id)

    def test_assigns_ip(self):
        self._builder.build_cluster()
        verify(self._network).assign_ip(self._server1)
        verify(self._network).assign_ip(self._server2)

    def test_waits_for_nodes(self):
        self._builder.build_cluster()
        servers = [self._server1, self._server2]
        verify(self._node_checker).wait_for_nodes(servers)

    def test_creates_files_with_hosts(self):
        self._builder.build_cluster()
        verify(self._file_generator).create_host_files([self._server1,
                                                        self._server2])

    def test_logs(self):
        self._builder.build_cluster()
        verify(self._logger).info("Configuring network...")
        verify(self._logger).info("Configuring security...")
        verify(self._logger).info("Booting VMs...")
        verify(self._logger).info("Assigning IP addresses...")
        verify(self._logger).info("Waiting for nodes to boot...")
        verify(self._logger).info("Generating host files...")

    def test_sets_logger_level(self):
        verify(self._logger).setLevel(logging.DEBUG)

    def test_logs_exceptions(self):
        e = Exception("error message")
        when(self._network).setup_network().thenRaise(e)
        self._builder.build_cluster()
        verify(self._logger).info(e)
        verify(self._logger).info("Exiting...")

    def _given_security_service(self):
        self._security = Mock()
        when_create_security = when(self._factory).create_security_service()
        when_create_security.thenReturn(self._security)

    def _given_network_service(self):
        self._network = Mock()
        self._network_id = "network id"
        when_network_service = when(self._factory).create_network_service()
        when_network_service.thenReturn(self._network)
        when(self._network).setup_network().thenReturn(self._network_id)

    def _given_servers_service(self):
        self._servers = Mock()
        self._server1 = Mock()
        self._server2 = Mock()
        when_create_servers = when(self._factory).create_server_service()
        when_create_servers.thenReturn(self._servers)
        when_boot = when(self._servers).boot_servers(10, self._network_id)
        when_boot.thenReturn([self._server1, self._server2])

    def _given_node_checker(self):
        self._node_checker = Mock()
        when_create = when(self._factory).create_node_checker()
        when_create.thenReturn(self._node_checker)

    def _given_file_generator(self):
        self._file_generator = Mock()
        when_create_generator = when(self._factory).create_file_generator()
        when_create_generator.thenReturn(self._file_generator)
