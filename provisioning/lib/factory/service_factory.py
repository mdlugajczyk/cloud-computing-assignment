from network_service import NetworkService
from api_client_factory import ApiClientFactory


class ServiceFactory:

    @staticmethod
    def create_network_service():
        quantum = ApiClientFactory.create_quantum_client()
        return NetworkService(quantum)
    


