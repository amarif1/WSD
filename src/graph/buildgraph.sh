#!/bin/bash

FILENAME=$1
count=0
cat $FILENAME | while read LINE
do
	let count++
	echo -ne "["$count"]:Building co-occurrence graph for word "$LINE" @ "
	date
	time ./src/buildgraph.py $LINE | tee log/$LINE.log
	echo -ne "["$count"]:Done! @ "
	date
done