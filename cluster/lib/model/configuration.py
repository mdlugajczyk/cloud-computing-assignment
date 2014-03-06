from os.path import expanduser


class Configuration:

    def __init__(self, ssh_key=None, ssh_key_name=None, image_name=None,
                 flavor=None):
        self._set_value_or_defautl("ssh_key", ssh_key, self._ssh_key_path())
        self._set_value_or_defautl("ssh_key_name", ssh_key_name,
                                   "s210664-key")
        self._set_value_or_defautl("image_name", image_name, "ubuntu-precise")
        self._set_value_or_defautl("flavor", flavor, "3")
        self.username = "ubuntu"
        self.mpiuser = "mpiuser"
        self.ssh_private_key = self.ssh_key.replace(".pub", "")

    def _set_value_or_defautl(self, var, val, default):
        if val:
            setattr(self, var, val)
        else:
            setattr(self, var, default)

    def _ssh_key_path(self):
        return expanduser("~/.ssh/id_rsa.pub")
