#!/bin/bash

## Finds which nodes are unreachable within private network.
## SSH to first node from hosts file, and try to ping each other node.
## If node is unreachable, return it's name.


if [ -ne $# 2 ]
then
    echo "Usage: $0 machinefile";
    exit 1
fi

hosts=$(nova list |grep s210664)
ips=$(nova list |grep 210664 | awk '{print $12}');
root_node=$(cat $1 | head -n 1)

echo "Unreachable VMs:"
for str in $ips
do
    ip=$(ruby -e "a = '$str'; puts a[a.index('=')+1..a.length-2]")
    ping_result=$(ssh $root_node "ping -c 4 $ip" | grep "Destination Host Unreachable")
    if [ -n "$ping_result" ]
    then
	echo "$hosts" | grep  $ip | awk '{print $4}'
    fi
done
