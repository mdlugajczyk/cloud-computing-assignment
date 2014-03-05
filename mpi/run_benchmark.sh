#!/bin/bash

function generate_input {
    if [ ! -f $1 ]
then
    ./generate $2 $3 > $1
fi  
}

if [ $# -ne 3 ]
then
    echo "Usage: $0 nodes rows cols";
    exit 1;
fi

INPUT1="input1_$2_$3.txt"
INPUT2="input2_$2_$3.txt"
OUTPUT="output_$2_$2.txt"

echo "Compiling program..."
make all 1> /dev/null;

echo "Generating input files..."
generate_input $INPUT1 $2 $3
generate_input $INPUT2 $2 $3

echo "Uploading executable to nodes..."
while read host; do
    scp multiply $host: 1> /dev/null
done < ../mpi.host

root_node=$(cat ../mpi.host |head -n 1)
scp $INPUT1 $root_node:
scp $INPUT2 $root_node:

mpirun -n $1 -machinefile ../mpi.host ./multiply $INPUT1 $INPUT2 $OUTPUT
