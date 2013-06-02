#!/bin/bash

USERNAME=$1
PASSWD=$2
FILENAME=$3
count=0
cat $FILENAME | while read LINE
do
	./src/verifycorp.py $USERNAME $PASSWD $LINE
done