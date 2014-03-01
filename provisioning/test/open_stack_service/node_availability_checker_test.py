import unittest
from lib.open_stack_service.node_availability_checker import NodeAvailabilityChecker, NodeConnectionException
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
        self._ssh = Mock()
        self._conf = Configuration()
        self._key = self._conf.ssh_private_key
        self._server1 = Server(ip=SERVER1_IP)
        self._server2 = Server(ip=SERVER2_IP)
        self._checker = NodeAvailabilityChecker(self._ssh, self._conf)

    def test_tries_ssh_into_nodes(self):
        self._wait_for_nodes_with_mocked_sleep()
        verify(self._ssh).connect(SERVER1_IP, username=self._conf.username,
                                  key_filename=self._key,
                                  timeout=2)
        verify(self._ssh).connect(SERVER2_IP, username=self._conf.username,
                                  key_filename=self._key,
                                  timeout=2)

    def test_retries_when_connection_timeout(self):
        when(self._ssh).connect(any(), username=any(),
                                key_filename=any(),
                                timeout=any()).thenRaise(socket.timeout).thenReturn(None).thenRaise(socket.timeout).thenReturn(None)
        self._wait_for_nodes_with_mocked_sleep()
        verify(self._ssh, times=2).connect(SERVER1_IP,
                                             username=self._conf.username,
                                             key_filename=self._key,
                                             timeout=2)
        verify(self._ssh, times=2).connect(SERVER2_IP,
                                             username=self._conf.username,
                                             key_filename=self._key,
                                             timeout=2)

    def test_waits_before_trying_another_connection(self):
        when(self._ssh).connect(any(), username=any(),
                                key_filename=any(),
                                timeout=any()).thenRaise(socket.timeout).thenReturn(None)
        mocked_sleep = mock_Mock()
        with patch('time.sleep', mocked_sleep):
            self._checker.wait_for_nodes([self._server1])
        mocked_sleep.assert_called_with(10)

    def test_stops_retries_after_timeout(self):
        mocked_time = mock_Mock()
        mocked_time.side_effect=self._update_time
        with patch('time.time', mocked_time):
            try:
                self._wait_for_nodes_with_mocked_sleep()
                raise Exception("Should throw timeout exception")
            except NodeConnectionException:
                pass

    def test_sets_missing_host_policy(self):
        verify(self._ssh).set_missing_host_key_policy(any(paramiko.AutoAddPolicy))
        
    def _wait_for_nodes_with_mocked_sleep(self):
        mocked_sleep = mock_Mock()
        with patch('time.sleep', mocked_sleep):
            self._checker.wait_for_nodes([self._server1, self._server2])

    def _update_time(self):
        self._current_time += TIMEOUT
        return self._current_time

    
        
