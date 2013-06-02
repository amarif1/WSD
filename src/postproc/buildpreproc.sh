#!/bin/bash

FILENAME=$1
count=0
cat $FILENAME | while read LINE
do
	let count++
	echo -ne "["$count"]:Building MST for word "$LINE" @ "
	date
	time ./postproc.py $LINE | tee log/$LINE.log
	echo -ne "["$count"]:Done! @ "
	date
done