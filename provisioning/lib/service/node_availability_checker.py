import socket
import time
import paramiko

TIMEOUT = 60*5

class NodeConnectionException(Exception):
    pass

class NodeAvailabilityChecker:
    
    def __init__(self, ssh_client, configuration):
        self._ssh = ssh_client
        self._conf = configuration
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def wait_for_nodes(self, nodes):
        self._start_time = time.time()
        for node in nodes:
            self._ssh_to_node(node)

    def _ssh_to_node(self, node):
        while self._timeout():
            if self._try_ssh_to_node(node):
                return
        raise NodeConnectionException()

    def _try_ssh_to_node(self, node):
        try:
            self._ssh.connect(node.ip, username=self._conf.username,
                              key_filename=self._conf.ssh_private_key,
                              timeout=2)
            return True
        except Exception:
            time.sleep(10)
            return False


    def _timeout(self):
        return time.time() - self._start_time < TIMEOUT
