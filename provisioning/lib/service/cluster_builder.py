import logging


class ClusterBuilder:

    def __init__(self, service_factory, logger):
        self._network = service_factory.create_network_service()
        self._security = service_factory.create_security_service()
        self._servers_service = service_factory.create_server_service()
        self._node_checker = service_factory.create_node_checker()
        self._file_generator = service_factory.create_file_generator()
        self._logger = logger
        self._logger.setLevel(logging.DEBUG)

    def build_cluster(self):
        try:
            self._try_build_cluster()        
        except Exception, e:
            self._logger.info(e)
            self._logger.info("Exiting...")
            
    def _try_build_cluster(self):
        self._setup_network()
        self._setup_security()
        self._boot_vms()
        self._assign_ip()
        self._wait_for_nodes()
        self._generate_host_files()
        
    def _setup_network(self):
        self._logger.info("Configuring network...")
        self._network_id = self._network.setup_network()

    def _setup_security(self):
        self._logger.info("Configuring security...")
        self._security.setup_security()

    def _boot_vms(self):
        self._logger.info("Booting VMs...")
        self._servers = self._servers_service.boot_servers(10,
                                                          self._network_id)
        
    def _assign_ip(self):
        self._logger.info("Assigning IP addresses...")
        for server in self._servers:
            self._network.assign_ip(server)

    def _wait_for_nodes(self):
        self._logger.info("Waiting for nodes to boot...")
        self._node_checker.wait_for_nodes(self._servers)

    def _generate_host_files(self):
        self._logger.info("Generating host files...")
        self._file_generator.create_host_files(self._servers)
