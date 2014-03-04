#!/bin/bash

INPUT1=m1.txt
INPUT2=m2.txt
OUTPUT=output.txt

if [ $# -ne 2 ]
then
    echo "Usage: $0 rows cols"
fi

make 1> /dev/null;
./generate $1 $2 > $INPUT1
./generate $1 $2 > $INPUT2
./multiply $INPUT1 $INPUT2 $OUTPUT
