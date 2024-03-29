import unittest
from lib.service.node_availability_checker import NodeAvailabilityChecker
from lib.model.configuration import Configuration
from lib.model.server import Server
from mockito import Mock, verify, when, any
from mock import patch, Mock as mock_Mock
import socket
import paramiko

SERVER1_IP = "10.7.2.130"
SERVER2_IP = "10.7.2.131"
TIMEOUT = 60*5


class NodeAvailabilityCheckerTest(unittest.TestCase):

    def setUp(self):
        self._current_time = 10
        self._mocked_sleep = mock_Mock()
        self._ssh = Mock()
        self._conf = Configuration()
        self._key = self._conf.ssh_private_key
        self._server1 = Server(name="server 1", ip=SERVER1_IP)
        self._server2 = Server(name="server 2", ip=SERVER2_IP)
        self._logger = Mock()
        self._checker = NodeAvailabilityChecker(self._ssh,
                                                self._conf, self._logger)

    def test_tries_ssh_into_nodes(self):
        self._wait_for_nodes_with_mocked_sleep([self._server1,
                                                self._server2])
        self._verify_connects_to_nodes_required_number_of_times(1)


    def test_retries_when_connection_timeout(self):
        self._when_connection_timeouts_for_first_time()
        self._wait_for_nodes_with_mocked_sleep([self._server1,
                                                self._server2])
        self._verify_connects_to_nodes_required_number_of_times(2)

    def test_logs_failure(self):
        self._when_connection_timeouts_for_first_time()
        self._wait_for_nodes_with_mocked_sleep([self._server1,
                                                self._server2])
        self._verify_logs_failures(2)

    def test_logs_success(self):
        nodes = [self._server1, self._server2]
        self._when_connection_timeouts_for_first_time()
        self._wait_for_nodes_with_mocked_sleep(nodes)
        self._verify_logs_nodes_available(nodes)
        
    def test_waits_before_trying_another_connection(self):
        self._when_connection_timeouts_for_first_time()
        self._wait_for_nodes_with_mocked_sleep([self._server1])
        self._mocked_sleep.assert_called_with(2)

    def test_logs_connection_attempts(self):
        self._wait_for_nodes_with_mocked_sleep([self._server1])
        message = "Waiting for %s at %s to become available..."
        verify(self._logger).info(message % (self._server1.name,
                                             self._server1.ip))

    def test_sets_missing_host_policy(self):
        policy = paramiko.AutoAddPolicy
        verify(self._ssh).set_missing_host_key_policy(any(policy))
        
    def _wait_for_nodes_with_mocked_sleep(self, nodes):        
        with patch('time.sleep', self._mocked_sleep):
            self._checker.wait_for_nodes(nodes)

    def _update_time(self):
        self._current_time += TIMEOUT
        return self._current_time

    def _verify_connects_to_nodes_required_number_of_times(self, t):
        verify(self._ssh, times=t).connect(SERVER1_IP,
                                           username=self._conf.username,
                                           key_filename=self._key,
                                           timeout=2)
        verify(self._ssh, times=t).connect(SERVER2_IP,
                                           username=self._conf.username,
                                           key_filename=self._key,
                                           timeout=2)

    def _verify_logs_failures(self, t):
        verify(self._logger, times=t).info("Connection failed.")

    def _verify_logs_nodes_available(self, nodes):
        for node in nodes:
            message = "Server %s is available." % node.name 
            verify(self._logger).info(message)
        
    def _when_connection_timeouts_for_first_time(self):
        when_connect = when(self._ssh).connect(any(), username=any(),
                                               key_filename=any(),
                                               timeout=any())
        first_timeout = when_connect.thenRaise(socket.timeout)
        second_timeout = first_timeout.thenRaise(socket.timeout)
        second_timeout.thenReturn(None)
