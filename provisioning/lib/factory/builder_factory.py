import logging
from lib.factory.service_factory import ServiceFactory
from lib.service.cluster_builder import ClusterBuilder

class BuilderFactory:

    @staticmethod
    def create_builder():
        service_factory = ServiceFactory()
        logging.basicConfig(format='%(message)s')
        logger = logging.getLogger("logger")
        logger.setLevel(logging.DEBUG)
        return  ClusterBuilder(service_factory, logger)

