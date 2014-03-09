# Installation

This project comes with Makefile, to build all binaries invoke:

	$ make all

It will create to executables: generate and multiply.
Generates creates random matrix of given dimensions.
Multiply multiplies two matrices.

# Scripts

Two scripts have been created for this project. One runs multiplication of
two specified matrices, the other automates process of generating data
for the report.

run_benchmark.sh can be used as follows:

	$ ./run_benchmark.sh number_of_nodes machinefile input1 input2 container output

run.sh can be used as follows:

	$ ./run.sh number_of_nodes machinefile


# Unreachable nodes

In order to automate identifying unreachable nodes (due to the private network problem) `find_unreachable_nodes.sh` script has been created.

It assumes that first node in machine file is working properly.

It can be used as follows:

	$ ./find_unreachable_nodes.sh machinefile

It will print names and IDs of unreachable nodes.
