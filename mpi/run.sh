#!/bin/bash

### Automates usage of run_benchmark.sh by generating
### input files with required dimensions.

function generate_input {
    if [ ! -f $1 ]
    then
	./generate $2 $3 > $1
    fi  
}

if [ $# -ne 4 ]
then
    echo "Usage: $0 nodes machinefile rows cols ";
    exit 1;
fi

rows=$3
cols=$4
input1="input1-$rows-$cols.txt"
input2="input2-$rows-$cols.txt"
output="output-$rows-$cols.txt"

hosts_file=$2
container="test-container"

echo "Generating input files..."
generate_input $input1 $rows $cols
generate_input $input2 $rows $cols

echo "Starting run_bechmark..."
./run_benchmark.sh $1 $hosts_file $input1 $input2 $container $output
