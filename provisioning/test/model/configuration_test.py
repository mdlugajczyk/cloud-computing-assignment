import unittest
from os.path import expanduser
from lib.model.configuration import Configuration


class ConfigurationTest(unittest.TestCase):

    def test_has_default_value_for_ssh_key(self):
        config = Configuration()
        self.assertEqual(config.ssh_key, expanduser("~/.ssh/id_rsa.pub"))

    def test_can_set_value_for_ssh_key(self):
        config = Configuration(ssh_key="/some/path")
        self.assertEqual(config.ssh_key, "/some/path")

    def test_has_default_value_for_ssh_key_name(self):
        config = Configuration()
        self.assertEqual(config.ssh_key_name, "s210664-key")

    def test_can_set_value_for_ssh_key_name(self):
        config = Configuration(ssh_key_name="keyname")
        self.assertEqual(config.ssh_key_name, "keyname")

    def test_has_default_value_for_image_name(self):
        config = Configuration()
        self.assertEqual(config.image_name, "ubuntu-precise")

    def test_can_set_value_for_image_name(self):
        config = Configuration(image_name="image name")
        self.assertEqual(config.image_name, "image name")
