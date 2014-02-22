class ServerService:

    def __init__(self, servers_manager, images_manager,
                 key_name, image_name):
        self._servers_manager = servers_manager
        self._images_manager = images_manager
        self._key = key_name
        self._image_name = image_name

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
            if image.name == self._image_name:
                return image.id

    def _boot_server(self, index, image, network):
        nics = [{"net-id": network}]
        return self._servers_manager.create("s210664-vm-%d" % index,
                                            image, "1", nics=nics,
                                            key_name=self._key)
