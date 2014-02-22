import unittest
from lib.open_stack_service.server import ServerService
from novaclient.v1_1.images import Image
from mockito import Mock, verify, any, when


KEY_NAME = "key_name"
IMAGE_ID = "image id"
IMAGE_NAME = "ubuntu-precise"
NETWORK = "network id"


class ServerServiceTest(unittest.TestCase):

    def setUp(self):
        self._servers_manager = Mock()
        self._images_manager = Mock()
        self._setup_images_manager()
        self._service = ServerService(self._servers_manager,
                                      self._images_manager,
                                      KEY_NAME, IMAGE_NAME)

    def test_creates_required_number_of_servers(self):
        servers = self._boot_servers(3)
        self.assertEqual(3, len(servers))

    def test_boots_machines(self):
        self._boot_servers(3)
        for i in range(3):
            verify(self._servers_manager).create("s210664-vm-%d" % (i),
                                                 any(), "1", nics=any(),
                                                 key_name=any())

    def test_creates_vms_with_proper_key(self):
        self._boot_servers(1)
        verify(self._servers_manager).create(any(), any(), any(), nics=any(),
                                             key_name=KEY_NAME)

    def test_creates_vm_with_proper_image(self):
        self._boot_servers(1)
        verify(self._servers_manager).create(any(), IMAGE_ID, any(),
                                             nics=any(), key_name=any())

    def test_creates_vm_on_right_network(self):
        self._boot_servers(1)
        verify(self._servers_manager).create(any(), any(), any(),
                                             nics=[{"net-id": NETWORK}],
                                             key_name=any())

    def _setup_images_manager(self):
        image_list = [Image(Mock(), {"id": IMAGE_ID, "name": IMAGE_NAME}),
                      Image(Mock(), {"id": "image id", "name": "image"})]
        when(self._images_manager).list().thenReturn(image_list)

    def _boot_servers(self, number_servers):
        return self._service.boot_servers(number_servers, NETWORK)
