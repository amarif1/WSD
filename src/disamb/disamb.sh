#!/bin/bash

FILENAME=$1
cat $FILENAME | while read LINE
do
	python disamb.py palm """$LINE"""
done