from lib.model.server import Server


class ServerService:

    def __init__(self, servers_manager, images_manager, configuration):
        self._servers_manager = servers_manager
        self._images_manager = images_manager
        self._config = configuration

    def delete_vms(self):
        servers = self._servers_manager.list()
        for server in servers:
            server.delete()

    def boot_servers(self, number_servers, network):
        image = self._image_id()
        return self._boot_servers_with_image(image, number_servers, network)

    def _boot_servers_with_image(self, image, number_servers, network):
        servers = []
        for i in range(number_servers):
            server = self._boot_server(i, image, network)
            servers.append(server)
        return servers

    def _image_id(self):
        for image in self._images_manager.list():
            if image.name == self._config.image_name:
                return image.id

    def _boot_server(self, index, image, network):
        nics = [{"net-id": network}]
        server = self._servers_manager.create("s210664-vm-%d" % index,
                                            image, "3", nics=nics,
                                            key_name=self._config.ssh_key_name)
        return Server(name=server.name, id=server.id)
