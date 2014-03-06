import unittest
from os.path import expanduser
from lib.model.configuration import Configuration


class ConfigurationTest(unittest.TestCase):

    def setUp(self):
        self._config = Configuration()

    def test_has_default_value_for_ssh_key(self):
        self.assertEqual(self._config.ssh_key,
                         expanduser("~/.ssh/id_rsa.pub"))

    def test_can_set_value_for_ssh_key(self):
        config = Configuration(ssh_key="/some/path")
        self.assertEqual(config.ssh_key, "/some/path")

    def test_has_default_value_for_ssh_key_name(self):
        self.assertEqual(self._config.ssh_key_name, "s210664-key")

    def test_can_set_value_for_ssh_key_name(self):
        config = Configuration(ssh_key_name="keyname")
        self.assertEqual(config.ssh_key_name, "keyname")

    def test_has_default_value_for_image_name(self):
        self.assertEqual(self._config.image_name, "ubuntu-precise")

    def test_can_set_value_for_image_name(self):
        config = Configuration(image_name="image name")
        self.assertEqual(config.image_name, "image name")

    def test_has_default_value_for_ssh_user_name(self):
        self.assertEqual(self._config.username, "ubuntu")

    def test_has_default_value_for_ssh_private_key(self):
        self.assertEqual(self._config.ssh_private_key,
                         expanduser("~/.ssh/id_rsa"))

    def test_has_default_value_for_mpiuser(self):
        self.assertEqual(self._config.mpiuser, "mpiuser")

    def test_has_default_value_for_vm_flavor(self):
        self.assertEqual(self._config.flavor, "3")

    def test_can_set_value_for_vm_flavor(self):
        config = Configuration(flavor="2")
        self.assertEqual(config.flavor, "2")
