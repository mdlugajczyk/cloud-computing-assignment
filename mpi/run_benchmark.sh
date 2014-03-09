#!/bin/bash

if [ $# -ne 6 ]
then
    echo "Usage: $0 nodes machinefile input1 input2 container output";
    echo "$#";
    exit 1;
fi

nodes=$1
machinefile=$2
input1=$3
input2=$4
container=$5
output=$6

echo "Compiling program..."
make all 1> /dev/null

echo "Uploading executable to nodes..."
hosts=$(cat $machinefile)
for host in $hosts
do
    scp multiply $host: 1> /dev/null
done

echo "Uploading input files to root node..."
root_node=$(cat $machinefile |head -n 1)

## remove directories from input path
matrix1=$(basename $input1)
matrix2=$(basename $input2)

scp $input1 $root_node:$matrix1 1> /dev/null
scp $input2 $root_node:$matrix2 1> /dev/null

echo "Running the mpi program..."
mpirun -n $1 -machinefile $machinefile ./multiply $matrix1 $matrix2 $output

echo "Downloading output file..."
scp $root_node:$output $output 1> /dev/null

echo "Uploading results to swift..."
swift upload $container $output 1> /dev/null

echo "Done."
