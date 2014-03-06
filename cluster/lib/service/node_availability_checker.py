import socket
import time
import paramiko

TIMEOUT = 60*5


class NodeAvailabilityChecker:
    
    def __init__(self, ssh_client, configuration, logger):
        self._ssh = ssh_client
        self._conf = configuration
        self._logger = logger
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def wait_for_nodes(self, nodes):
        all_nodes = list(nodes)
        self._start_time = time.time()
        while self._timeout() and len(all_nodes) > 0:
            for node in all_nodes:
                self._ssh_to_node(node)
                if node.available:
                    all_nodes.remove(node)

    def _ssh_to_node(self, node):
        message = "Waiting for %s at %s to become available..."
        self._logger.info(message % (node.name, node.ip))
        if self._try_ssh_to_node(node):
            node.available = True
            self._logger.info("Server %s is available." % node.name)
        else:
            self._logger.info("Connection failed.")

    def _try_ssh_to_node(self, node):
        try:
            self._ssh.connect(node.ip, username=self._conf.username,
                              key_filename=self._conf.ssh_private_key,
                              timeout=2)
            return True
        except Exception:
            time.sleep(2)
            return False

    def _timeout(self):
        return time.time() - self._start_time < TIMEOUT
