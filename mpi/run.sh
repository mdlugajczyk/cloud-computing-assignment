#!/bin/bash

### Automates usage of run_benchmark.sh by generating
### input files with required dimensions.

function generate_input {
    if [ ! -f $1 ]
    then
	./generate $2 $3 > $1
    fi  
}

if [ $# -ne 2 ]
then
    echo "Usage: $0 nodes machinefile ";
    exit 1;
fi

nodes=$1
hosts_file=$2
container="s210664-results"

echo "Generating input files..."
generate_input $input1 $rows $cols
generate_input $input2 $rows $cols


for size in 128 256 512 1024 2048; do
    input1="inputs/input1-$size-$size.txt"
    input2="inputs/input2-$size-$size.txt"
    generate_input $input1 $size $size;
    generate_input $input2 $size $size;

    for i in 1 2 3 4 5; do
	output="output-$i-$size-$size-$nodes.txt"
	echo "Iteration $i for problem size $size..."
	./run_benchmark.sh $nodes $hosts_file $input1 $input2 $container $output	
    done
    
done


