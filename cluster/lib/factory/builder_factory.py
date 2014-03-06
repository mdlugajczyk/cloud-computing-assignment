from lib.factory.service_factory import ServiceFactory
from lib.service.cluster_builder import ClusterBuilder

class BuilderFactory:

    @staticmethod
    def create_builder(flavor):
        service_factory = ServiceFactory(flavor)
        logger = service_factory.create_logger()
        return  ClusterBuilder(service_factory, logger)

