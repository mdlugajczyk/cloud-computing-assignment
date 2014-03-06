class FileGenerator:

    def __init__(self, configuration):
        self._conf = configuration
        
    def create_host_files(self, nodes):
        self._create_ansible_file(nodes)
        self._create_mpi_file(nodes)

    def _create_mpi_file(self, nodes):
        with open('mpi.host', 'w') as f:
            self._write_mpi_nodes(f, nodes)

    def _write_mpi_nodes(self, f, nodes):
        node_format = "%s@%s\n"
        for node in nodes:
            f.write(node_format % (self._conf.mpiuser,
                                   node.ip))
    
    def _create_ansible_file(self, nodes):
        with open('ansible_mpi.host', 'w') as f:
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
