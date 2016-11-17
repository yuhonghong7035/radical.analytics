#!/bin/sh

src=' \(agent_0:MainThread,pilot.[0-9]\+,PMGR_ACTIVE,\)'
tgt=',\1'
root='.'
files=$(find $root -name agent_0.prof -print)
for file in $files
do
    echo $file
    sed -i'' "s/$src/$tgt/g" $file
done

