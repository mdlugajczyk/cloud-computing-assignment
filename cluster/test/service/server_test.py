import unittest
from mockito import Mock, verify, any, when
from mock import Mock as mockMock
from novaclient.v1_1.images import Image
from novaclient.v1_1.servers import Server as NovaServer
from lib.service.server import ServerService
from lib.model.configuration import Configuration

IMAGE_ID = "image id"
NETWORK = "network id"
SERVER_ID = "server id"
SERVER_NAME = "sever name"

class ServerServiceTest(unittest.TestCase):

    def setUp(self):
        self._servers_manager = Mock()
        self._images_manager = Mock()
        self._conf = Configuration()
        self._setup_images_manager()
        server = NovaServer(Mock(), {"name": SERVER_NAME, "id": SERVER_ID})
        when(self._servers_manager).create(any(), any(), any(), nics=any(),
                                           key_name=any()).thenReturn(server)
        self._service = ServerService(self._servers_manager,
                                      self._images_manager,
                                      self._conf)

    def test_creates_required_number_of_servers(self):
        servers = self._boot_servers(3)
        self.assertEqual(3, len(servers))

    def test_boots_machines(self):
        self._boot_servers(3)
        for i in range(3):
            verify(self._servers_manager).create("s210664-vm-%d" % (i),
                                                 any(), "3", nics=any(),
                                                 key_name=any())

    def test_creates_vms_with_proper_key(self):
        self._boot_servers(1)
        verify(self._servers_manager).create(any(), any(), any(), nics=any(),
                                             key_name=self._conf.ssh_key_name)

    def test_creates_vm_with_proper_image(self):
        self._boot_servers(1)
        verify(self._servers_manager).create(any(), IMAGE_ID, any(),
                                             nics=any(), key_name=any())

    def test_creates_vm_on_right_network(self):
        self._boot_servers(1)
        verify(self._servers_manager).create(any(), any(), any(),
                                             nics=[{"net-id": NETWORK}],
                                             key_name=any())

    def test_destroys_created_vms(self):
        server1 = mockMock()
        server2 = mockMock()
        server1.name = "s210664-vm-0"
        server1.name = "s210664-vm-1"
        when(self._servers_manager).list().thenReturn([server1, server2])
        self._service.delete_vms()
        server1.delete.assert_called_once_with()
        server2.delete.assert_called_once_with()

    def test_returns_created_servers(self):
        servers = self._boot_servers(1)
        server = servers[0]
        self.assertEquals(server.name, SERVER_NAME)
        self.assertEquals(server.id, SERVER_ID)

    def _setup_images_manager(self):
        image_list = [Image(Mock(), {"id": IMAGE_ID,
                                     "name": self._conf.image_name}),
                      Image(Mock(), {"id": "image id", "name": "image"})]
        when(self._images_manager).list().thenReturn(image_list)


    def _boot_servers(self, number_servers):
        return self._service.boot_servers(number_servers, NETWORK)
