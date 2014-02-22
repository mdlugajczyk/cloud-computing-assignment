from factory.service_factory import ServiceFactory

service_factory = ServiceFactory()
net_service = service_factory.create_network_service()
net_service.setup_network()

sec_service = service_factory.create_security_service()
sec_service.setup_security()


