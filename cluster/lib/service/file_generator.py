class FileGenerator:
    """
    Generates host files for mpi and ansible.
    File names are specified by the configuration object.
    """

    def __init__(self, configuration):
        """
        Creates new instance of FileGenerator

        :param configuration: Configuration object with names of host files.
        """
        self._conf = configuration

    def create_host_files(self, nodes):
        """
        Creates two host files - one for mpi, one for ansible.

        :param nodes: Servers to be included in host files.
        """
        self._create_ansible_file(nodes)
        self._create_mpi_file(nodes)

    def _create_mpi_file(self, nodes):
        with open(self._conf.mpi_hosts_file, 'w') as f:
            self._write_mpi_nodes(f, nodes)

    def _write_mpi_nodes(self, f, nodes):
        node_format = "%s@%s\n"
        for node in nodes:
            f.write(node_format % (self._conf.mpiuser,
                                   node.ip))
    
    def _create_ansible_file(self, nodes):
        with open(self._conf.ansible_hosts_file, 'w') as f:
            self._write_ansible_header(f)
            self._write_ansible_nodes(f, nodes)

    def _write_ansible_nodes(self, f, nodes):
        for node in nodes:
            self._write_ansible_node(f, node)
                
    def _write_ansible_node(self, f, node):
        node_format = "%s ansible_ssh_host=%s ansible_ssh_user=%s\n"
        f.write(node_format % (node.name,
                               node.ip,
                               self._conf.username))

    def _write_ansible_header(self, f):
        f.write('[mpi_nodes]\n')
