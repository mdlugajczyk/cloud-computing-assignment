# Installation

To install dependencies required to run the project, invoke:

	$ ./install_dependencies.sh

It will download and install all required python packages.
It also installs all dependencies required to run unit tests.

Use of python's virtualenv is encouraged to avoid polluting system configuration.

# Usage

To run the script, inoke:

	$ python create_cluster number_of_nodes flavour


It will create required number of machines and provision them with MPI.

Network infrastructure: network, sub-net, router is reused - if script finds
that given infrastructure element with the same name already exists, it'll
reuse it. Names of all elements are prefixed with student number.

To avoid problems with ssh (which is used by ansible), ensure that ~/.ssh/known_hosts
does not contain IP addresses assigned by open stack to newly created machines.
Otherwise ansible will fail to connect to the nodes.

Script will generate two 'host' files, one for ansible, one for MPI.
MPI host file is used by the `run_benchmark.sh` and `run.sh` scripts.

To delete cluster, run:

	$ ./delete_cluster.sh

It will find all nodes with name prefixed by student number, theirs floating IPs
and delete them. Network infrastructure will not be deleted.


# Handling node failures

Script will handle nodes failure. If any node will fail to boot and become
available before timeout, program will proceed with remaining nodes
and provision them using ansible.

Status of the booted servers is not checked.

# Running tests

To run tests, invoke:

	$ nosetests

from `cluster` directory.
