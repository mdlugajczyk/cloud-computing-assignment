from factory.service_factory import ServiceFactory

service = ServiceFactory.create_network_service()
service.setup_network()

