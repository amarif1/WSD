#!/bin/bash

USERNAME=$1
PASSWD=$2
FILENAME=$3
count=0
cat $FILENAME | while read LINE
do
	let count++
	echo -ne "["$count"]:Building corpus for word "$LINE" @ "
	date
	time ./src/buildcorp.py $USERNAME $PASSWD $LINE | tee log/$LINE.log
	echo -ne "["$count"]:Done! @ "
	date
done