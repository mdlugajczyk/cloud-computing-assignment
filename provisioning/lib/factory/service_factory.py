from network_service import NetworkService
from security_service import SecurityService
from api_client_factory import ApiClientFactory


class ServiceFactory:

    def __init__(self):
        self._api_factory = ApiClientFactory()
    
    def create_network_service(self):
        quantum = self._api_factory.create_quantum_client()
        return NetworkService(quantum)

    def create_security_service(self):
        groups_manager = self._api_factory.create_security_groups_manager()
        rules_manager = self._api_factory.create_security_rules_manager()
        return SecurityService(groups_manager, rules_manager)
        
