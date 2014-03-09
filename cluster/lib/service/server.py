from lib.model.server import Server
import time


class ServerService:
    """
    Provides abstraction over open stack APIs to boot VMs.
    """

    def __init__(self, servers_manager, images_manager, configuration):
        """
        Creates new instance of ServerService.

        :param servers_manager: Manager for open stack server.
        :param images_manager: Manager for open stack server's images.
        :param configuration: Configuration object.
        """
        self._servers_manager = servers_manager
        self._images_manager = images_manager
        self._config = configuration

    def delete_vms(self):
        """
        Deletes all created open stack instances."
        """
        servers = self._servers_manager.list()
        for server in servers:
            server.delete()

    def boot_servers(self, number_servers, network):
        """
        Boots open stack instances inside network.

        In order to avoid exceeding the limit of created instances per
        time unit, script calls sleep(5) after each booted instance.

        :param number_servers: Number of instances to boot.
        :param network: Network for instances.
        """
        image = self._image_id()
        return self._boot_servers_with_image(image, number_servers, network)

    def _boot_servers_with_image(self, image, number_servers, network):
        servers = []
        for i in range(number_servers):
            server = self._boot_server(i, image, network)
            time.sleep(5)
            servers.append(server)
        return servers

    def _image_id(self):
        for image in self._images_manager.list():
            if image.name == self._config.image_name:
                return image.id

    def _boot_server(self, index, image, network):
        nics = [{"net-id": network}]
        key = self._config.ssh_key_name
        server = self._servers_manager.create("s210664-vm-%d" % index,
                                              image,
                                              self._config.flavor,
                                              nics=nics,
                                              key_name=key)
        return Server(name=server.name, id=server.id)
