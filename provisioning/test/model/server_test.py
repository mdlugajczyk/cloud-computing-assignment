import unittest
from lib.model.server import Server

class ServerTest(unittest.TestCase):

    def setUp(self):
        self._server = Server(name="name", address="192.168.1.1", id="id")
        
    def test_have_name(self):
        self.assertEqual(self._server.name, "name")

    def test_have_address(self):
        self.assertEqual(self._server.address, "192.168.1.1")

    def test_have_id(self):
        self.assertEqual(self._server.id, "id")

