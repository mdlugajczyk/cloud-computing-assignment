import unittest
from lib.service.file_generator import FileGenerator
from lib.model.configuration import Configuration
from lib.model.server import Server
from mock import Mock, mock_open, patch, call

class FileGeneratorTest(unittest.TestCase):

    def setUp(self):
        self._server1 = Server(name="server1", ip="ip1")
        self._server2 = Server(name="server2", ip="ip2")
        self._open = mock_open()
        self._file_handle = self._open.return_value.__enter__.return_value
        self._conf = Configuration()
        self._generator = FileGenerator(self._conf)

    def test_open_ansible_host_file(self):
        self._generate_files()
        ansible_hosts_file = call('ansible_mpi.host', 'w') 
        self.assertTrue(ansible_hosts_file in self._open.call_args_list)

    def test_open_mpi_host_file(self):
        self._generate_files()
        mpi_hosts_file = call('mpi.host', 'w') 
        self.assertTrue(mpi_hosts_file in self._open.call_args_list)

    def test_writes_mpi_hosts(self):
        self._generate_files()
        self._verify_called_with("%s@%s\n" % (self._conf.username,
                                            self._server1.ip))
        self._verify_called_with("%s@%s\n" % (self._conf.username,
                                              self._server2.ip))

    def test_writes_ansible_header(self):
        self._generate_files()
        self._verify_called_with('[mpi_nodes]\n')

    def test_writes_ansible_hosts(self):
        self._generate_files()
        node_format = "%s ansible_ssh_host=%s ansible_ssh_user=%s\n"
        self._verify_called_with(node_format % (self._server1.name,
                                                self._server1.ip,
                                                self._conf.username))
        self._verify_called_with(node_format % (self._server2.name,
                                                self._server2.ip,
                                                self._conf.username))

    def test_writes_mpi_header(self):
        pass
    
    def _generate_files(self):
        with patch('__builtin__.open', self._open):
            self._generator.create_host_files([self._server1, self._server2])

    def _verify_called_with(self, arg):
        calls = self._file_handle.write.call_args_list
        self.assertTrue(call(arg) in calls, "Expected call with: %s" % arg)
