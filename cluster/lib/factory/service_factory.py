from lib.service.mpi_deployer import MpiDeployer
from lib.service.network import NetworkService
from lib.service.security import SecurityService
from lib.service.server import ServerService
from lib.service.file_generator import FileGenerator
from lib.service.node_availability_checker import NodeAvailabilityChecker
import paramiko
import logging
from lib.model.configuration import Configuration
from api_client_factory import ApiClientFactory


class ServiceFactory:

    def __init__(self, flavor):
        self._api_factory = ApiClientFactory()
        self._config = Configuration(flavor=flavor)

    def create_network_service(self):
        quantum = self._api_factory.create_quantum_client()
        return NetworkService(quantum)

    def create_security_service(self):
        groups_manager = self._api_factory.create_security_groups_manager()
        rules_manager = self._api_factory.create_security_rules_manager()
        keypairs_manager = self._api_factory.create_keypairs_manager()
        return SecurityService(groups_manager, rules_manager,
                               keypairs_manager, self._config)

    def create_server_service(self):
        servers_manager = self._api_factory.create_servers_manager()
        images_manager = self._api_factory.create_images_manager()
        return ServerService(servers_manager, images_manager, self._config)

    def create_node_checker(self):
        ssh = paramiko.SSHClient()
        return NodeAvailabilityChecker(ssh, self._config,
                                       self.create_logger())

    def create_file_generator(self):
        return FileGenerator(self._config)

    def create_mpi_deployer(self):
        return MpiDeployer(self._config)

    def create_logger(self):
        logging.basicConfig(format='%(message)s')
        return logging.getLogger("cluster_builder_logger")
